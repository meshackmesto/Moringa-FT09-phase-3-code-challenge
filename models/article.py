from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        if id is None:
            self._save_to_db()

    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author = cursor.fetchone()
        conn.close()
        if author:
            return Author(author['id'], author['name'])
        return None

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        if magazine:
            return Magazine(magazine['id'], magazine['name'], magazine['category'])
        return None
