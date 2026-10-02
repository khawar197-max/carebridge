from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from database.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(150), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(30), nullable=True)
    emergency_contact = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=True)
    document_date = Column(Date, nullable=True)
    extracted_text = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    status = Column(String(50), default="PENDING")
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    session_id = Column(String(100), nullable=True)
    user_message = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=True)
    agent_name = Column(String(100), nullable=True)
    risk_level = Column(String(30), default="LOW")
    created_at = Column(DateTime, default=datetime.utcnow)


class CareTask(Base):
    __tablename__ = "care_tasks"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    priority = Column(String(30), default="MEDIUM")
    status = Column(String(30), default="PROPOSED")
    created_by_agent = Column(String(100), nullable=True)
    approved_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    specialty = Column(String(100), nullable=True)
    provider_name = Column(String(150), nullable=True)
    purpose = Column(String(255), nullable=True)
    status = Column(String(30), default="SCHEDULED")
    created_at = Column(DateTime, default=datetime.utcnow)


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    memory_type = Column(String(50), nullable=False)
    memory_key = Column(String(100), nullable=False)
    memory_value = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    patient_id = Column(Integer, nullable=True)
    agent_name = Column(String(100), nullable=True)
    action = Column(String(100), nullable=False)
    input_reference = Column(Text, nullable=True)
    output_reference = Column(Text, nullable=True)
    approval_status = Column(String(30), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
