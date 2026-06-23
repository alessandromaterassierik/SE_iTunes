from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def load_albums(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, title, sum(t.milliseconds/60000) as durata
                from album a
                join track t on a.id = t.album_id
                group by t.album_id having sum(t.milliseconds/60000) > %s """

        cursor.execute(query, (durata,))
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def load_tuple_albums(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                
with playlistAlbum as (select pt.playlist_id, t.album_id
                    from playlist_track pt
                    join track t on pt.track_id = t.id),
             		
albumsFiltered as (select a.id, title
from album a
join track t on a.id = t.album_id
group by t.album_id having sum(t.milliseconds/60000) > %s )
    
select distinct a1.album_id as a1, a2.album_id as a2
from playlistAlbum a1
join playlistAlbum a2 on a1.playlist_id = a2.playlist_id
where a1.album_id > a2.album_id and a1.album_id in (select af.id from albumsFiltered af)
and a2.album_id in (select af.id from albumsFiltered af)
                    """

        cursor.execute(query, (durata,))
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result