import os

from flask import Blueprint, request, current_app as app
from werkzeug.utils import secure_filename

from director.db import load_db
from director.handler import ChatHandler, SessionHandler, VideoDBHandler, ConfigHandler


agent_bp = Blueprint("agent", __name__, url_prefix="/agent")
session_bp = Blueprint("session", __name__, url_prefix="/session")
videodb_bp = Blueprint("videodb", __name__, url_prefix="/videodb")
config_bp = Blueprint("config", __name__, url_prefix="/config")
voice_bp = Blueprint("voice", __name__, url_prefix="/voice")


@agent_bp.route("/", methods=["GET"], strict_slashes=False)
def agent():
    """
    Handle the agent request
    """
    chat_handler = ChatHandler(
        db=load_db(os.getenv("SERVER_DB_TYPE", app.config["DB_TYPE"]))
    )
    return chat_handler.agents_list()


@session_bp.route("/", methods=["GET"], strict_slashes=False)
def get_sessions():
    """
    Get all the sessions
    """
    session_handler = SessionHandler(
        db=load_db(os.getenv("SERVER_DB_TYPE", app.config["DB_TYPE"]))
    )
    return session_handler.get_sessions()


@session_bp.route("/<session_id>", methods=["GET", "DELETE"])
def get_session(session_id):
    """
    Get or delete the session details
    """
    if not session_id:
        return {"message": f"Please provide {session_id}."}, 400

    session_handler = SessionHandler(
        db=load_db(os.getenv("SERVER_DB_TYPE", app.config["DB_TYPE"]))
    )
    session = session_handler.get_session(session_id)
    if not session:
        return {"message": "Session not found."}, 404

    if request.method == "GET":
        return session
    elif request.method == "DELETE":
        success, failed_components = session_handler.delete_session(session_id)
        if success:
            return {"message": "Session deleted successfully."}, 200
        else:
            return {
                "message": f"Failed to delete the entry for following components: {', '.join(failed_components)}"
            }, 500


@videodb_bp.route("/collection", defaults={"collection_id": None}, methods=["GET"])
@videodb_bp.route("/collection/<collection_id>", methods=["GET"])
def get_collection_or_all(collection_id):
    """Get a collection by ID or all collections."""
    videodb = VideoDBHandler(collection_id)
    if collection_id:
        return videodb.get_collection()
    else:
        return videodb.get_collections()


@videodb_bp.route("/collection", methods=["POST"])
def create_collection():
    try:
        data = request.get_json()

        if not data or not data.get("name"):
            return {"message": "Collection name is required"}, 400

        if not data.get("description"):
            return {"message": "Collection description is required"}, 400

        collection_name = data["name"]
        description = data["description"]

        videodb = VideoDBHandler()
        result = videodb.create_collection(collection_name, description)

        if result.get("success"):
            return {"message": "Collection created successfully", "data": result}, 201
        else:
            return {
                "message": "Failed to create collection",
                "error": result.get("error"),
            }, 400
    except Exception as e:
        return {"message": str(e)}, 500


@videodb_bp.route("/collection/<collection_id>", methods=["DELETE"])
def delete_collection(collection_id):
    try:
        if not collection_id:
            return {"message": "Collection ID is required"}, 400

        videodb = VideoDBHandler(collection_id)
        result = videodb.delete_collection()
        return result, 200
    except Exception as e:
        return {"message": str(e)}, 500


@videodb_bp.route(
    "/collection/<collection_id>/video", defaults={"video_id": None}, methods=["GET"]
)
@videodb_bp.route("/collection/<collection_id>/video/<video_id>", methods=["GET"])
def get_video_or_all(collection_id, video_id):
    """Get a video by ID or all videos in a collection."""
    videodb = VideoDBHandler(collection_id)
    if video_id:
        return videodb.get_video(video_id)
    else:
        return videodb.get_videos()
    
@videodb_bp.route(
    "/collection/<collection_id>/audio", defaults={"audio_id": None}, methods=["GET"]
)
@videodb_bp.route("/collection/<collection_id>/audio/<audio_id>", methods=["GET"])
def get_audio_or_all(collection_id, audio_id, **kwargs):
    """Get a video by ID or all videos in a collection."""
    videodb = VideoDBHandler(collection_id)
    if audio_id:
        return videodb.get_audio(audio_id)
    else:
        return videodb.get_audios()


@videodb_bp.route(
    "/collection/<collection_id>/image", defaults={"image_id": None}, methods=["GET"]
)
@videodb_bp.route("/collection/<collection_id>/image/<image_id>", methods=["GET"])
def get_image_or_all(collection_id, image_id, **kwargs):
    """Get a video by ID or all videos in a collection."""
    videodb = VideoDBHandler(collection_id)
    if image_id:
        return videodb.get_image(image_id)
    else:
        return videodb.get_images()



@videodb_bp.route("/collection/<collection_id>/video/<video_id>", methods=["DELETE"])
def delete_video(collection_id, video_id):
    """Delete a video by ID from a specific collection."""
    try:
        if not video_id:
            return {"message": "Video ID is required"}, 400
        videodb = VideoDBHandler(collection_id)
        result = videodb.delete_video(video_id)
        return result, 200
    except Exception as e:
        return {"message": str(e)}, 500


@videodb_bp.route("/collection/<collection_id>/audio/<audio_id>", methods=["DELETE"])
def delete_audio(collection_id, audio_id):
    """Delete a audio by ID from a specific collection."""
    try:
        if not audio_id:
            return {"message": "Video ID is required"}, 400
        videodb = VideoDBHandler(collection_id)
        result = videodb.delete_audio(audio_id)
        return result, 200
    except Exception as e:
        return {"message": str(e)}, 500


@videodb_bp.route("/collection/<collection_id>/image/<image_id>", methods=["DELETE"])
def delete_image(collection_id, image_id):
    """Delete a image by ID from a specific collection."""
    try:
        if not image_id:
            return {"message": "Video ID is required"}, 400
        videodb = VideoDBHandler(collection_id)
        result = videodb.delete_image(image_id)
        return result, 200
    except Exception as e:
        return {"message": str(e)}, 500


@videodb_bp.route(
    "/collection/<collection_id>/image/<image_id>/generate_url", methods=["GET"]
)
def generate_image_url(collection_id, image_id):
    try:
        if not collection_id:
            return {"message": "Collection ID is required"}, 400

        if not image_id:
            return {"message": "Image ID is required"}, 400

        videodb = VideoDBHandler(collection_id)
        result = videodb.generate_image_url(image_id)
        return result, 200
    except Exception as e:
        return {"message": str(e)}, 500

@videodb_bp.route(
    "/collection/<collection_id>/audio/<audio_id>/generate_url", methods=["GET"]
)
def generate_audio_url(collection_id, audio_id):
    try:
        if not collection_id:
            return {"message": "Collection ID is required"}, 400

        if not audio_id:
            return {"message": "Audio ID is required"}, 400

        videodb = VideoDBHandler(collection_id)
        result = videodb.generate_audio_url(audio_id)
        return result, 200
    except Exception as e:
        return {"message": str(e)}, 500

@videodb_bp.route("/collection/<collection_id>/upload", methods=["POST"])
def upload_video(collection_id):
    """Upload a video to a collection."""
    try:
        videodb = VideoDBHandler(collection_id)

        if "file" in request.files:
            file = request.files["file"]
            file_bytes = file.read()
            safe_filename = secure_filename(file.filename)
            if not safe_filename:
                return {"message": "Invalid filename"}, 400
            file_name = os.path.splitext(safe_filename)[0]
            media_type = file.content_type.split("/")[0]
            return videodb.upload(
                source=file_bytes,
                source_type="file",
                media_type=media_type,
                name=file_name,
            )
        elif "source" in request.json:
            source = request.json["source"]
            source_type = request.json["source_type"]
            return videodb.upload(source=source, source_type=source_type)
        else:
            return {"message": "No valid source provided"}, 400
    except Exception as e:
        return {"message": str(e)}, 500


@config_bp.route("/check", methods=["GET"])
def config_check():
    config_handler = ConfigHandler()
    return config_handler.check()


# Voice Chat API Endpoints

@voice_bp.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """Transcribe audio file to text using Whisper API."""
    try:
        from director.agents.voice_chat import VoiceChatAgent
        from director.core.session import Session
        
        if "file" not in request.files:
            return {"message": "Audio file is required", "error": "no_file"}, 400
        
        audio_file = request.files["file"]
        if audio_file.filename == "":
            return {"message": "No audio file selected", "error": "empty_file"}, 400
        
        # Read audio bytes
        audio_bytes = audio_file.read()
        
        # Create a temporary session for voice processing
        session = Session()
        voice_agent = VoiceChatAgent(session=session)
        
        # Transcribe using agent
        response = voice_agent._transcribe_audio(audio_input=audio_bytes)
        
        if response:
            return {"success": True, "transcription": response}, 200
        else:
            return {"success": False, "message": "Failed to transcribe audio"}, 400
            
    except Exception as e:
        return {"success": False, "message": str(e), "error": "transcription_failed"}, 500


@voice_bp.route("/speech", methods=["POST"])
def generate_speech():
    """Generate speech from text using TTS API."""
    try:
        from director.agents.voice_chat import VoiceChatAgent
        from director.core.session import Session
        
        data = request.get_json()
        if not data or not data.get("text"):
            return {"message": "Text is required", "error": "no_text"}, 400
        
        text = data.get("text")
        voice_id = data.get("voice_id", "default")
        
        if len(text) > 5000:
            return {"message": "Text exceeds maximum length (5000 characters)"}, 400
        
        # Create a temporary session for voice processing
        session = Session()
        voice_agent = VoiceChatAgent(session=session)
        
        # Generate speech
        audio_path = voice_agent._generate_speech(text, voice_id)
        
        if audio_path:
            return {"success": True, "audio_url": audio_path}, 200
        else:
            return {"success": False, "message": "Failed to generate speech"}, 400
            
    except Exception as e:
        return {"success": False, "message": str(e), "error": "speech_generation_failed"}, 500


@voice_bp.route("/chat", methods=["POST"])
def voice_chat():
    """Full voice chat handler - transcribe, process, and generate response."""
    try:
        from director.agents.voice_chat import VoiceChatAgent
        from director.core.session import Session
        
        if "audio" not in request.files:
            return {"message": "Audio file is required", "error": "no_file"}, 400
        
        audio_file = request.files["audio"]
        if audio_file.filename == "":
            return {"message": "No audio file selected", "error": "empty_file"}, 400
        
        # Optional response text for TTS
        response_text = request.form.get("response_text")
        voice_id = request.form.get("voice_id", "default")
        generate_speech = request.form.get("generate_speech", "true").lower() == "true"
        
        # Read audio bytes
        audio_bytes = audio_file.read()
        
        # Create a temporary session for voice processing
        session = Session()
        voice_agent = VoiceChatAgent(session=session)
        
        # Process voice chat
        result = voice_agent.run(
            audio_input=audio_bytes,
            generate_speech_response=generate_speech,
            response_text=response_text,
            voice_id=voice_id
        )
        
        if result.status == "success":
            return {"success": True, "data": result.data}, 200
        else:
            return {"success": False, "message": result.message}, 400
            
    except Exception as e:
        return {"success": False, "message": str(e), "error": "voice_chat_failed"}, 500
