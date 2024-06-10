from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        if id is None:
            self._save_to_db()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def _save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self.name, self.category))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    @property
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]

    def article_titles(self):
        articles = self.articles
        if articles:
            return [article.title for article in articles]
        return None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        if authors:
            return [Author(author['id'], author['name']) for author in authors]
        return None
