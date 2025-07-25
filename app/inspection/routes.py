from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.inspection.validators import validate_image_url
from app.models.inspection import Inspection
from . import inspection_bp

@inspection_bp.route('/', methods=["POST"])
@jwt_required()
def create_new_inspection():
    """Create a new inspection entry"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        vehicle_number = data.get('vehicle_number')
        damage_report = data.get('damage_report')
        image_url = data.get('image_url')
        
        if not vehicle_number:
            return jsonify({'error': 'Vehicle number is required'}), 400
            
        if not damage_report:
            return jsonify({'error': 'Damage report is required'}), 400
        
        if not image_url:
            return jsonify({'error': 'Image url is required'}), 400
        
        if image_url and not validate_image_url(image_url):
            return jsonify({'error': 'Invalid image URL. Must end with .jpg, .jpeg, or .png'}), 400
        
        # Create new inspection
        inspection = Inspection(
            vehicle_number=vehicle_number,
            inspected_by=current_user_id,
            damage_report=damage_report,
            image_url=image_url,
            status='pending'
        )
        
        db.session.add(inspection)
        db.session.commit()
        
        current_app.logger.info(f'Inspection created: ID {inspection.id} by user {current_user_id}')
        
        return jsonify({
            'message': 'Inspection created successfully',
            'inspection': {
                'id': inspection.id,
                'vehicle_number': inspection.vehicle_number,
                'damage_report': inspection.damage_report,
                'status': inspection.status,
                'image_url': inspection.image_url,
                'created_at': inspection.created_at.isoformat()
            }
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Database error creating inspection: {str(e)}')
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        current_app.logger.error(f'Error creating inspection: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500