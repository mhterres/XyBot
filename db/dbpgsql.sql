--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: xybot
--

CREATE SEQUENCE logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000
    CACHE 1;


ALTER TABLE logs_id_seq OWNER TO xybot;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: muc_chat; Type: TABLE; Schema: public; Owner: xybot
--

CREATE TABLE muc_chat (
    id bigint DEFAULT nextval('logs_id_seq'::regclass) NOT NULL,
    date timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    nick character varying(50) NOT NULL,
    msg_from character varying(150),
    message text NOT NULL,
    msg_to character varying(150)
);


ALTER TABLE muc_chat OWNER TO xybot;

--
-- Name: users_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: xybot
--

CREATE SEQUENCE users_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000
    CACHE 1;


ALTER TABLE users_logs_id_seq OWNER TO xybot;

--
-- Name: users_logs; Type: TABLE; Schema: public; Owner: xybot
--

CREATE TABLE users_logs (
    id bigint DEFAULT nextval('users_logs_id_seq'::regclass) NOT NULL,
    date timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    nick character varying(50) NOT NULL,
    operation character varying(15) NOT NULL,
    jid character varying(150)
);


ALTER TABLE users_logs OWNER TO xybot;

--
-- Name: logs_pkey; Type: CONSTRAINT; Schema: public; Owner: xybot
--

ALTER TABLE ONLY muc_chat
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- Name: users_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: xybot
--

ALTER TABLE ONLY users_logs
    ADD CONSTRAINT users_logs_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

