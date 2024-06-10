from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        if id is None:
            self._save_to_db()

    def __repr__(self):
        return f'<Author {self.name}>'

    def _save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self.name,))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    @property
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id 
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]
