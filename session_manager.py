import datetime

class ChatSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.context = {}
        self.last_interaction_time = None

    def update_context(self, key, value):
        self.context[key] = value

    def get_context(self, key):
        return self.context.get(key)

    def start_session(self):
        # Initialize the session, e.g., set start time
        self.last_interaction_time = get_current_time()

    def end_session(self):
        # Clean up resources or perform any necessary actions when the session ends
        pass

    def is_session_expired(self, max_inactive_time):
        # Check if the session has been inactive for too long
        current_time = get_current_time()
        return (current_time - self.last_interaction_time) > max_inactive_time


class ChatSessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        if session_id not in self.sessions:
            new_session = ChatSession(session_id)
            new_session.start_session()
            self.sessions[session_id] = new_session

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def end_session(self, session_id):
        session = self.sessions.get(session_id)
        if session:
            session.end_session()
            del self.sessions[session_id]

    def is_session_expired(self, session_id, max_inactive_time=30*60):
        session = self.sessions.get(session_id)
        return session and session.is_session_expired(max_inactive_time)

    def update_context(self, session_id, key, value):
        session = self.sessions.get(session_id)
        if session:
            session.update_context(key, value)

    def get_context(self, session_id, key):
        session = self.sessions.get(session_id)
        if session is  None:
            return None
        return session.get_context(key)
    
    def cleanup_expired_sessions(self, max_inactive_time=30*60):
        expired_sessions = [session_id for session_id, session in self.sessions.items() if session.is_session_expired(max_inactive_time)]
        
        for session_id in expired_sessions:
            self.end_session(session_id)

def get_current_time():
    return datetime.datetime.now()