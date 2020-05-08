import datetime
from . import db, bcrypt


class Hash(db.Model):
    """A wifi hash with optional cracked counterpart"""

    id = db.Column(db.Integer, primary_key=True)
    pcap = db.Column(
        db.String(3500000), nullable=False
    )  # stored in string as base64, max 2.5mb
    jobs = db.relationship("Job")  # passwords
    reports = db.relationship("Report")
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, pcap: str, password: str = None):
        self.pcap = pcap

        if password:
            self.password = password

        self.created = datetime.datetime.utcnow()


class Client(db.Model):
    """A single client connected to api"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(512), nullable=True)
    jobs = db.relationship("Job")
    reports = db.relationship("Report")
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username: str, password: str, bio: str = None):
        self.username = username
        self.password = self.gen_password(password)

        if bio:
            self.bio = bio

        self.created = datetime.datetime.utcnow()

    def gen_password(self, plaintext_password: str) -> str:
        """Generates a hash from a plaintext password provided"""

        return bcrypt.generate_password_hash(plaintext_password)

    def compare_passwords(self, comparison: str):
        """Compare password on file to a given password"""

        return bcrypt.check_password_hash(self.password, comparison)


class Job(db.Model):
    """A finished job (password) related to a client and a hash"""

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(1024), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    hash_id = db.Column(db.Integer, db.ForeignKey("hash.id"), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, password: str):
        self.password = password
        self.created = datetime.datetime.utcnow()


class Report(db.Model):
    """A reported hash for job, this is for when bad jobs are assigned and a
    client reports it as bad"""

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    hash_id = db.Column(db.Integer, db.ForeignKey("hash.id"), nullable=False)
    info = db.Column(db.String(256), nullable=True)  # optional info field
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, info: str = None):
        self.info = info
        self.created = datetime.datetime.utcnow()
