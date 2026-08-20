from app.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship


class Post(Base): 
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone= True),server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable=False)
    
    
    # Relación ORM: cada post tiene un "owner" (usuario). Conecta con User.posts
    owner = relationship("User", back_populates="posts", passive_deletes=True)


    # El método __repr__ define cómo se mostrará el objeto cuando lo imprimas.
    # Sirve para depuración y legibilidad en la consola.
    # Aquí devolvemos una cadena con el id y el título del post.
    def __repr__(self):
        return f"<Post id={self.id} title={self.title!r} content={self.content!r}>"
    
    
    """recordad que cada vez que vamos a agregar una columna con alchemy no deberia existir esa tabla
    ya que no la generara, por eso la manera eficiente de hacer esas migraciones en con alembic"""
    
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone= True),server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    
    # Relación inversa: un usuario puede tener muchos posts
    posts = relationship("Post", back_populates="owner")
    

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r} password={self.password!r}>"
    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key= True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key=True)