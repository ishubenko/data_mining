from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

engine = create_engine('sqlite:///gb_blog.db')
models.Base.metadata.create_all(bind=engine)
SessionMaker = sessionmaker(bind=engine)
# def get_db():
#     db = SessionMaker()
#     try:
#         yield db
#     finally:
#         db.close()
if __name__ == '__main__':
    print(1)