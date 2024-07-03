# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlite3


class MoviesweeklyscraperPipeline:
    def process_item(self, item, spider):
        item = self.clean_title(item)
        item = self.clean_original_title(item)
        item = self.clean_score_press(item)
        item = self.clean_score_spectator(item)
        item = self.clean_duration(item)
        item = self.clean_year(item)
        item = self.clean_gender(item)
        item = self.clean_director(item)
        item = self.clean_public(item)
        item = self.clean_nationality(item)
        item = self.clean_description(item)
        item = self.clean_distributor(item)
        item = self.clean_production_year(item)
        item = self.clean_actors(item)
        # item = self.clean_scriptwriter(item)
        return item
    
    def clean_title(self, item):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        if title is not None:
            match = re.search(r'>(.*?)<', title)
            if match:
                adapter['title'] = match.group(1)
        return item

    def clean_original_title(self, item):
        adapter = ItemAdapter(item)
        original_title = adapter.get('original_title')
        if original_title and 'Titre' in original_title[-2]:
            value = original_title[-1]
        else:
            value = adapter.get('title')
        adapter['original_title'] = value
        return item

    def clean_score_press(self, item):
        adapter = ItemAdapter(item)
        press_score = adapter.get('press_score')
        if press_score is not None:
            adapter['press_score'] = float(press_score.replace(',', '.'))
        return item

    def clean_score_spectator(self, item):
        adapter = ItemAdapter(item)
        spectator_score = adapter.get('spectator_score')
        if spectator_score is not None:
            adapter['spectator_score'] = float(spectator_score.replace(',', '.'))
        return item
    
    def clean_duration(self, item):
        if isinstance(item['duration'], list):
            duration = ''.join(item['duration']).strip()
        else:
            duration = item['duration'].strip()

        hours = re.search(r'(\d+)h', duration)
        minutes = re.search(r'(\d+)min', duration)
        total_minutes = 0
        if hours:
            total_minutes += int(hours.group(1)) * 60
        if minutes:
            total_minutes += int(minutes.group(1))

        item['duration'] = total_minutes
        return item

    def clean_year(self, item):
        adapter = ItemAdapter(item)
        year = adapter.get('year')
        if year:
            cleaned_year = year.strip().replace('\n', '')
            match = re.search(r'\b\d{4}\b', cleaned_year)
            if match:
                cleaned_year = match.group(0)
            else:
                cleaned_year = '' 

            adapter['year'] = cleaned_year
        return item

    def clean_gender(self, item):
        adapter = ItemAdapter(item)
        gender = adapter.get('gender')
        if gender:
            cleaned_gender = [gender_type.strip('|').strip() for gender_type in gender if gender_type.strip('|').strip()]
            adapter['gender'] = cleaned_gender
        return item

    def clean_director(self, item):
        adapter = ItemAdapter(item)
        directors = adapter.get('director')
        # if director:
        #    director_name = director[1:director.index('Par')]
        # else:
        #     director_name = ''
        # adapter['director'] = director_name
        # return item
        if directors:
            directors = list(director for director in directors if '\n' not in director)
            adapter['director'] = directors[:2]
        return item
    
    def clean_public(self, item):
        adapter = ItemAdapter(item)
        public = adapter.get('public')
        adapter['public'] = public if public is not None else ''
        return item
    
    def clean_nationality(self, item):
        adapter = ItemAdapter(item)
        adapter.get('nationality')
        return item
    
    def clean_description(self, item):
        adapter = ItemAdapter(item)
        description = adapter.get('description')
        if description:
            adapter['description'] = ''.join(description).strip()
        return item
    
    def clean_distributor(self, item):
        adapter = ItemAdapter(item)
        distributor = adapter.get('distributor')
        if distributor:
            cleaned_distributor = distributor[-1].strip()
            adapter['distributor'] = cleaned_distributor
        return item
    
    def clean_production_year(self, item):
        adapter = ItemAdapter(item)
        production_year = adapter.get('production_year')
        if production_year:
            cleaned_production_year = production_year[-1].strip()
            adapter['production_year'] = cleaned_production_year
        return item
    
    def clean_actors(self, item):
        adapter = ItemAdapter(item)
        actors = adapter.get('actors')
        if actors:
            actors = list(actor for actor in actors if '\n' not in actor)
            adapter['actors'] = actors[:8]
        return item
    
    # def clean_scriptwriter(self, item):
    #     adapter = ItemAdapter(item)
    #     scriptwriters = adapter.get('actors')
    #     if scriptwriters:
    #         scriptwriters = list(scriptwriter for scriptwriter in scriptwriters if '\n' not in scriptwriter)
    #         adapter['scriptwriters'] = scriptwriters[:3]
    #     return item


class FilmDatabasePipeline:
    def open_spider(self, spider):        
        self.connection = sqlite3.connect('weeklymovies.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE weeklymovies")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS weeklymovies(
            id SERIAL PRIMARY KEY,
            title TEXT,
            original_title TEXT,
            score_press NUMERIC,
            score_spectator NUMERIC,
            duration INTEGER,
            year INTEGER,
            gender TEXT[],
            director TEXT[],
            public TEXT,
            nationality TEXT[],
            description TEXT,
            distributor TEXT,
            production_year INTEGER,
            actors TEXT[])
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.connection = sqlite3.connect('books.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            INSERT INTO weeklymovies(
            title,
            original_title,
            score_press,
            score_spectator,
            duration,
            year,
            gender,
            director,
            public,
            nationality,
            description,
            distributor,
            production_year,
            actors)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                (item['title'],
                item['original_title'],
                item['score_press'],
                item['score_spectator'],
                item['duration'],
                item['year'],
                item['gender'],
                item['director'],
                item['public'],
                item['nationality'],
                item['description'],
                item['distributor'],
                item['production_year'],
                item['actors'])
        )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()