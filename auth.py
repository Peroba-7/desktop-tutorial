from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import obter_sessao
from models import Utilizador

SECRET_KEY = "domo_secret_key_super_segura_para_o_leandro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def obter_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def criar_token_acesso(data: dict):
    dados_a_codificar = data.copy()
    exp_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_a_codificar.update({"exp": exp_at})
    return jwt.encode(dados_a_codificar, SECRET_KEY, algorithm=ALGORITHM)

def obter_utilizador_atual(token: str = Depends(oauth2_scheme), session: Session = Depends(obter_sessao)):
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais de autenticação inválidas ou expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credenciais_exception
    except JWTError:
        raise credenciais_exception
    
    statement = select(Utilizador).where(Utilizador.username == username)
    utilizador = session.exec(statement).first()
    if utilizador is None or not utilizador.ativo:
        raise credenciais_exception
    return utilizador