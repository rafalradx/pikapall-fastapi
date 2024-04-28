from sqlalchemy.orm import Session
from src.database.models import Comment
from datetime import datetime
from src.schemas.users import RoleEnum


def create_comment(db: Session, photo_id: int, user_id: int, content: str):
    """
    Funkcja tworząca nowy komentarz do zdjęcia.

    :param db: Sesja bazy danych.
    :param photo_id: Identyfikator zdjęcia.
    :param user_id: Identyfikator użytkownika, który dodaje komentarz.
    :param content: Treść komentarza.
    :return: Nowo utworzony obiekt komentarza.
    """
    new_comment = Comment(
        photo_id=photo_id,
        user_id=user_id,
        content=content,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def update_comment(db: Session, comment_id: int, user_id: int, new_content: str):
    """
    Funkcja aktualizująca treść komentarza.

    :param db: Sesja bazy danych.
    :param comment_id: Identyfikator komentarza do aktualizacji.
    :param user_id: Identyfikator użytkownika, który dodaje komentarz.
    :param new_content: Nowa treść komentarza.
    :return: Zaktualizowany obiekt komentarza lub None, jeśli użytkownik nie jest autorem komentarza.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment and comment.user_id == user_id:
        comment.content = new_content
        comment.updated_at = datetime.now()
        db.commit()
        db.refresh(comment)
        return comment
    return None


def delete_comment(db: Session, comment_id: int, user_role: RoleEnum):
    """
    Funkcja usuwająca komentarz.

    :param db: Sesja bazy danych.
    :param comment_id: Identyfikator komentarza do usunięcia.
    :param user_role: Rola użytkownika.
    :return: True, jeśli komentarz został pomyślnie usunięty, w przeciwnym razie False.
    """
    if user_role in [RoleEnum.admin, RoleEnum.mod]:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment:
            db.delete(comment)
            db.commit()
            return True
    return False


def get_comments_for_photo(db: Session, photo_id: int):
    """
    Funkcja zwracająca wszystkie komentarze dla danego zdjęcia.

    :param db: Sesja bazy danych.
    :param photo_id: Identyfikator zdjęcia.
    :return: Lista komentarzy dla danego zdjęcia.
    """
    return db.query(Comment).filter(Comment.photo_id == photo_id).all()
