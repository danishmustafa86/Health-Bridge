"""
AWS SES (Simple Email Service) Service
Handles email notifications and communications
"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from datetime import datetime

class SESService:
    """AWS SES service class for email operations"""
    
    def __init__(self):
        """Initialize SES service with AWS credentials"""
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@medcare.com")
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS credentials are required")
        
        try:
            self.ses_client = boto3.client(
                'ses',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
        except NoCredentialsError:
            raise ValueError("Invalid AWS credentials")
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send email using SES
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body (optional)
            from_email: Sender email (optional, uses default if not provided)
        
        Returns:
            Dict: SES response
        """
        try:
            sender = from_email or self.from_email
            
            # Construct email message
            message = {
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    }
                }
            }
            
            # Add HTML body if provided
            if body_html:
                message['Body']['Html'] = {
                    'Data': body_html,
                    'Charset': 'UTF-8'
                }
            
            # Send email
            response = self.ses_client.send_email(
                Source=sender,
                Destination={'ToAddresses': [to_email]},
                Message=message
            )
            
            return {
                'message_id': response['MessageId'],
                'status': 'sent',
                'timestamp': datetime.now().isoformat()
            }
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'MessageRejected':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email message rejected"
                )
            elif error_code == 'MailFromDomainNotVerified':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sender email domain not verified"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to send email: {str(e)}"
                )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Email sending failed: {str(e)}"
            )
    
    async def send_appointment_confirmation(
        self,
        patient_email: str,
        patient_name: str,
        doctor_name: str,
        appointment_date: str,
        appointment_time: str,
        consultation_fee: float
    ) -> Dict[str, Any]:
        """
        Send appointment confirmation email to patient
        
        Args:
            patient_email: Patient's email address
            patient_name: Patient's name
            doctor_name: Doctor's name
            appointment_date: Appointment date
            appointment_time: Appointment time
            consultation_fee: Consultation fee
        
        Returns:
            Dict: Email sending result
        """
        subject = "Appointment Confirmation - MedCare"
        
        body_text = f"""
        Dear {patient_name},
        
        Your appointment has been confirmed with the following details:
        
        Doctor: {doctor_name}
        Date: {appointment_date}
        Time: {appointment_time}
        Consultation Fee: ${consultation_fee}
        
        Please arrive 15 minutes early for your appointment.
        
        If you need to reschedule or cancel, please contact us at least 24 hours in advance.
        
        Thank you for choosing MedCare.
        
        Best regards,
        MedCare Team
        """
        
        body_html = f"""
        <html>
        <head></head>
        <body>
            <h2>Appointment Confirmation</h2>
            <p>Dear {patient_name},</p>
            <p>Your appointment has been confirmed with the following details:</p>
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Doctor:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{doctor_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Date:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{appointment_date}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Time:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{appointment_time}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Consultation Fee:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">${consultation_fee}</td>
                </tr>
            </table>
            <p><strong>Please arrive 15 minutes early for your appointment.</strong></p>
            <p>If you need to reschedule or cancel, please contact us at least 24 hours in advance.</p>
            <p>Thank you for choosing MedCare.</p>
            <p>Best regards,<br>MedCare Team</p>
        </body>
        </html>
        """
        
        return await self.send_email(patient_email, subject, body_text, body_html)
    
    async def send_diagnosis_notification(
        self,
        patient_email: str,
        patient_name: str,
        doctor_name: str,
        diagnosis: str
    ) -> Dict[str, Any]:
        """
        Send diagnosis notification email to patient
        
        Args:
            patient_email: Patient's email address
            patient_name: Patient's name
            doctor_name: Doctor's name
            diagnosis: Diagnosis details
        
        Returns:
            Dict: Email sending result
        """
        subject = "Diagnosis Available - MedCare"
        
        body_text = f"""
        Dear {patient_name},
        
        {doctor_name} has added a new diagnosis to your medical record:
        
        Diagnosis: {diagnosis}
        
        Please log in to your MedCare account to view the complete diagnosis details, including treatment plan and prescriptions.
        
        If you have any questions, please don't hesitate to contact your doctor.
        
        Best regards,
        MedCare Team
        """
        
        body_html = f"""
        <html>
        <head></head>
        <body>
            <h2>New Diagnosis Available</h2>
            <p>Dear {patient_name},</p>
            <p>{doctor_name} has added a new diagnosis to your medical record:</p>
            <div style="background-color: #f0f8ff; padding: 15px; border-left: 4px solid #0066cc; margin: 10px 0;">
                <strong>Diagnosis:</strong> {diagnosis}
            </div>
            <p>Please log in to your MedCare account to view the complete diagnosis details, including treatment plan and prescriptions.</p>
            <p>If you have any questions, please don't hesitate to contact your doctor.</p>
            <p>Best regards,<br>MedCare Team</p>
        </body>
        </html>
        """
        
        return await self.send_email(patient_email, subject, body_text, body_html)
    
    async def send_appointment_reminder(
        self,
        patient_email: str,
        patient_name: str,
        doctor_name: str,
        appointment_date: str,
        appointment_time: str
    ) -> Dict[str, Any]:
        """
        Send appointment reminder email to patient
        
        Args:
            patient_email: Patient's email address
            patient_name: Patient's name
            doctor_name: Doctor's name
            appointment_date: Appointment date
            appointment_time: Appointment time
        
        Returns:
            Dict: Email sending result
        """
        subject = "Appointment Reminder - MedCare"
        
        body_text = f"""
        Dear {patient_name},
        
        This is a friendly reminder about your upcoming appointment:
        
        Doctor: {doctor_name}
        Date: {appointment_date}
        Time: {appointment_time}
        
        Please arrive 15 minutes early for your appointment.
        
        If you need to reschedule or cancel, please contact us as soon as possible.
        
        Best regards,
        MedCare Team
        """
        
        body_html = f"""
        <html>
        <head></head>
        <body>
            <h2>Appointment Reminder</h2>
            <p>Dear {patient_name},</p>
            <p>This is a friendly reminder about your upcoming appointment:</p>
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Doctor:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{doctor_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Date:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{appointment_date}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"><strong>Time:</strong></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{appointment_time}</td>
                </tr>
            </table>
            <p><strong>Please arrive 15 minutes early for your appointment.</strong></p>
            <p>If you need to reschedule or cancel, please contact us as soon as possible.</p>
            <p>Best regards,<br>MedCare Team</p>
        </body>
        </html>
        """
        
        return await self.send_email(patient_email, subject, body_text, body_html)
    
    def verify_email_identity(self, email: str) -> Dict[str, Any]:
        """
        Verify email identity with SES
        
        Args:
            email: Email address to verify
        
        Returns:
            Dict: Verification result
        """
        try:
            response = self.ses_client.verify_email_identity(EmailAddress=email)
            return {
                'email': email,
                'status': 'verification_sent',
                'message': 'Verification email sent'
            }
        
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to verify email identity: {str(e)}"
            )
    
    def get_send_quota(self) -> Dict[str, Any]:
        """
        Get SES sending quota
        
        Returns:
            Dict: Sending quota information
        """
        try:
            response = self.ses_client.get_send_quota()
            return {
                'max_24_hour_send': response['Max24HourSend'],
                'max_send_rate': response['MaxSendRate'],
                'sent_last_24_hours': response['SentLast24Hours']
            }
        
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get send quota: {str(e)}"
            )