from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from logger import setup_logger

logger = setup_logger(__name__)

def generate_ticket_pdf(booking_details: dict, output_path: str):
    """Generates a PDF train ticket with booking details."""
    logger.info(f"Generating PDF ticket for PNR: {booking_details.get('pnr')}")
    
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        styles = getSampleStyleSheet()

        # Title
        title_style = styles['h1']
        title_style.alignment = 1 # Center alignment
        title = Paragraph("Train Ticket", title_style)
        title.wrapOn(c, width - 100, height)
        title.drawOn(c, 50, height - 50)

        # Booking Details
        c.drawString(50, height - 100, f"PNR: {booking_details.get('pnr', 'N/A')}")
        c.drawString(50, height - 120, f"Train: {booking_details.get('train_name', 'N/A')} ({booking_details.get('train_id', 'N/A')})")
        c.drawString(50, height - 140, f"Date of Journey: {booking_details.get('journey_date', 'N/A')}")
        c.drawString(50, height - 160, f"From: {booking_details.get('source_station_name', 'N/A')} ({booking_details.get('source_station_code', 'N/A')})")
        c.drawString(50, height - 180, f"To: {booking_details.get('destination_station_name', 'N/A')} ({booking_details.get('destination_station_code', 'N/A')})")
        c.drawString(50, height - 200, f"Booking Time: {booking_details.get('booking_time', 'N/A')}")
        c.drawString(50, height - 220, f"Status: {booking_details.get('status', 'N/A')}")

        # Passenger Details Table
        if booking_details.get('passengers'):
            c.drawString(50, height - 250, "Passenger Details:")
            
            data = [['Name', 'Age', 'Category']]
            for passenger in booking_details['passengers']:
                data.append([
                    passenger.get('name', 'N/A'),
                    passenger.get('age', 'N/A'),
                    passenger.get('category', 'N/A')
                ])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ]))

            # Calculate table size and draw it
            table_width, table_height = table.wrap(width, height)
            table.drawOn(c, 50, height - 270 - table_height)

        # Footer
        c.drawString(50, 50, "Thank you for booking with Rail Transit!")

        c.save()
        logger.info(f"PDF ticket generated successfully at: {output_path}")
        return {"success": True, "output_path": output_path}

    except Exception as e:
        logger.error(f"Error generating PDF ticket: {e}")
        return {"success": False, "error": str(e)}

# Example usage:
if __name__ == '__main__':
    dummy_booking_details = {
        'pnr': 'ABC123XYZ',
        'train_id': 'RX001',
        'train_name': 'Rajadhani Express',
        'journey_date': '2023-10-27',
        'source_station_code': 'SRC',
        'source_station_name': 'Source City',
        'destination_station_code': 'DEST',
        'destination_station_name': 'Destination City',
        'booking_time': '2023-10-26 10:00:00',
        'status': 'Confirmed',
        'passengers': [
            {'name': 'John Doe', 'age': 30, 'category': 'Adult'},
            {'name': 'Jane Smith', 'age': 8, 'category': 'Child'},
            {'name': 'Peter Jones', 'age': 65, 'category': 'Senior'},
        ]
    }
    output_dir = "tickets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, f"ticket_{dummy_booking_details['pnr']}.pdf")
    generate_ticket_pdf(dummy_booking_details, output_file) 