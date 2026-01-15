import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    ForeignKey,
    DECIMAL,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# =========================
# User Table
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    submitted_urls = relationship(
        "SubmittedURL",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================
# Submitted URLs Table
# =========================
class SubmittedURL(Base):
    __tablename__ = "submitted_urls"

    url_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    original_url = Column(Text, nullable=False)
    prediction = Column(
        Enum("safe", "malicious", name="prediction_enum", native_enum=False),
        nullable=False
    )
    confidence_score = Column(DECIMAL(5, 2))
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="submitted_urls")
    mutations = relationship(
        "PhishingLinkMutation",
        back_populates="submitted_url",
        cascade="all, delete-orphan"
    )
    logs = relationship(
        "DetectionLog",
        back_populates="submitted_url",
        cascade="all, delete-orphan"
    )


# =========================
# Phishing Link Mutations
# =========================
class PhishingLinkMutation(Base):
    __tablename__ = "phishing_link_mutations"

    mutation_id = Column(Integer, primary_key=True, autoincrement=True)
    original_url_id = Column(
        Integer,
        ForeignKey("submitted_urls.url_id"),
        nullable=False
    )

    mutated_url = Column(Text, nullable=False)
    mutation_type = Column(String(100))
    status = Column(
        Enum(
            "predicted",
            "blocked",
            "detected",
            name="mutation_status_enum",
            native_enum=False
        ),
        default="predicted"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    submitted_url = relationship("SubmittedURL", back_populates="mutations")


# =========================
# WHOIS / IP Information
# =========================
class WhoisIPInfo(Base):
    __tablename__ = "whois_ip_info"

    whois_id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(255), nullable=False)
    ip_address = Column(String(45))
    server = Column(String(255))
    port = Column(Integer)
    registrar = Column(String(255))
    country = Column(String(100))
    domain_age_days = Column(Integer)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())


# =========================
# URL ↔ WHOIS Mapping
# =========================
class URLWhoisMapping(Base):
    __tablename__ = "url_whois_mapping"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey("submitted_urls.url_id"), nullable=False)
    whois_id = Column(Integer, ForeignKey("whois_ip_info.whois_id"), nullable=False)


# =========================
# Detection Logs
# =========================
class DetectionLog(Base):
    __tablename__ = "detection_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey("submitted_urls.url_id"), nullable=False)

    action_taken = Column(String(100))
    decision_reason = Column(Text)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

    submitted_url = relationship("SubmittedURL", back_populates="logs")
