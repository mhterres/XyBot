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
-- Name: asterisk_xybot_id_seq; Type: SEQUENCE; Schema: public; Owner: asterisk_xybot
--

CREATE SEQUENCE asterisk_xybot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000000
    CACHE 1;


ALTER TABLE asterisk_xybot_id_seq OWNER TO asterisk_xybot;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: sip; Type: TABLE; Schema: public; Owner: asterisk_xybot
--

CREATE TABLE sip (
    id bigint DEFAULT nextval('asterisk_xybot_id_seq'::regclass) NOT NULL,
    name character varying(10) NOT NULL,
    callerid character varying(150) NOT NULL,
    xmpp_jid character varying(150),
    xmpp_allow_call boolean DEFAULT false NOT NULL,
    xmpp_allow_sms boolean DEFAULT false NOT NULL,
    xmpp_allow_admin_cmd boolean DEFAULT false NOT NULL
);


ALTER TABLE sip OWNER TO asterisk_xybot;

--
-- Name: sip_name_key; Type: CONSTRAINT; Schema: public; Owner: asterisk_xybot
--

ALTER TABLE ONLY sip
    ADD CONSTRAINT sip_name_key UNIQUE (name);


--
-- Name: sip_pkey; Type: CONSTRAINT; Schema: public; Owner: asterisk_xybot
--

ALTER TABLE ONLY sip
    ADD CONSTRAINT sip_pkey PRIMARY KEY (id);


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

