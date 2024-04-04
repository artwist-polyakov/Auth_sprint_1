CREATE SCHEMA IF NOT EXISTS content;

SET search_path TO content;

CREATE TABLE IF NOT EXISTS film_work ( id UUID PRIMARY KEY, title TEXT NOT NULL, description TEXT, creation_date DATE, file_path TEXT, rating FLOAT, type TEXT not null, created timestamp with time zone, modified timestamp with time zone );

CREATE TABLE IF NOT EXISTS genre ( id UUID PRIMARY KEY, name TEXT NOT NULL, description TEXT, created timestamp with time zone, modified timestamp with time zone );

CREATE TABLE IF NOT EXISTS genre_film_work ( id UUID PRIMARY KEY, film_work_id UUID NOT NULL, genre_id UUID NOT NULL, created timestamp with time zone );

CREATE TABLE IF NOT EXISTS person ( id UUID primary key, full_name text not null, created timestamp with time zone, modified timestamp with time zone );

CREATE TABLE IF NOT EXISTS person_film_work ( id UUID PRIMARY KEY, film_work_id UUID NOT NULL, person_id UUID NOT NULL, role TEXT NOT NULL, created timestamp with time zone );

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre ON genre_film_work (film_work_id, genre_id);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role ON person_film_work (film_work_id, person_id, role);
