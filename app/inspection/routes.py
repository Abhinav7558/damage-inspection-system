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
    

@inspection_bp.route('/<int:id>', methods=["GET"])
@jwt_required()
def fetch_inspection_details(id: int):
    """Fetch inspection details (only if created by the logged-in user)"""
    try:
        current_user_id = int(get_jwt_identity())

        inspection = Inspection.query.filter_by(
            id=id, 
            inspected_by=current_user_id
        ).first()

        if not inspection:
            return jsonify({'error': 'Inspection not found or unauthorized access'}), 404
            
        current_app.logger.info(f'Inspection {id} retrieved by user {current_user_id}')

        return jsonify({
            'inspection': {
                'id': inspection.id,
                'vehicle_number': inspection.vehicle_number,
                'damage_report': inspection.damage_report,
                'status': inspection.status,
                'image_url': inspection.image_url,
                'created_at': inspection.created_at.isoformat()
            }
        }), 200
        
    except SQLAlchemyError as e:
        current_app.logger.error(f'Database error fetching inspection: {str(e)}')
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        current_app.logger.error(f'Error fetching inspection: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
    

@inspection_bp.route('/<int:id>', methods=["PATCH"])
@jwt_required()
def update_inspection_status(id: int):
    """Update the status to reviewed or completed"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        new_status = data.get('status')
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        if new_status not in ['reviewed', 'completed']:
            return jsonify({'error': 'Invalid status. Must be pending, reviewed, or completed'}), 400

        inspection = Inspection.query.filter_by(
            id=id, 
            inspected_by=current_user_id
        ).first()

        if not inspection:
            return jsonify({'error': 'Inspection not found or unauthorized access'}), 404
        
        inspection.status = new_status
        db.session.commit()
            
        current_app.logger.info(f'Inspection {id} status updated to {new_status} by user {current_user_id}')

        return jsonify({
            'inspection': {
                'id': inspection.id,
                'vehicle_number': inspection.vehicle_number,
                'damage_report': inspection.damage_report,
                'status': inspection.status,
                'image_url': inspection.image_url,
                'created_at': inspection.created_at.isoformat()
            }
        }), 200
        
    except SQLAlchemyError as e:
        current_app.logger.error(f'Database error fetching inspection: {str(e)}')
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        current_app.logger.error(f'Error fetching inspection: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
        