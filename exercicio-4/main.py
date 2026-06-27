from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Config do JWT
SECRET_KEY = "sua_chave_secreta_segura" # cenário real: variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CRITÉRIO: Hash de senhas

# Configuração do passlib para usar o algoritmo bcrypt
def get_password_hash(password: str) -> str:
    # O bcrypt exige bytes, então codificamos a string
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Retornamos como string para salvar no nosso "banco de dados"
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

# Banco de dados simulado, memória local
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("senha123")
    }
}

# CRITÉRIO: Geração/validação JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Geração do Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# O OAuth2PasswordBearer extrai automaticamente o token do cabeçalho "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def validar_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Validação/Decodificação do Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # type: ignore
        if username is None:
            raise credentials_exception
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError:
        raise credentials_exception

# CRITÉRIO: Endpoint de login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    
    # Verifica se o usuário existe e se a senha descriptografada confere
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Retorna o JWT se autenticado com sucesso
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# CRITÉRIO: Proteção de endpoints

# O "Depends(validar_token)" atua como o middleware exigido: o código da função só executa se o token for validado com sucesso.
@app.post("/produtos")
def criar_produto(produto: dict, current_user: str = Depends(validar_token)):
    return {
        "mensagem": "Produto criado com sucesso!",
        "produto": produto,
        "usuario_responsavel": current_user
    }