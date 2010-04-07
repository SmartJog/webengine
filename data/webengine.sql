--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET check_function_bodies = false;
SET client_min_messages = warning;


--
-- Role: webengine
--

CREATE SCHEMA webengine;
CREATE ROLE webengine WITH PASSWORD 'webengine';
ALTER SCHEMA webengine OWNER TO webengine;
ALTER ROLE webengine WITH SUPERUSER LOGIN;
ALTER ROLE webengine SET search_path TO webengine, pg_catalog;
GRANT ALL ON SCHEMA webengine to webengine;


SET search_path = webengine, pg_catalog;

--
-- Name: auth_group; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_group (
    id serial NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE webengine.auth_group OWNER TO webengine;

--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_group', 'id'), 1, false);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_group_permissions (
    id serial NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE webengine.auth_group_permissions OWNER TO webengine;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_group_permissions', 'id'), 1, false);


--
-- Name: auth_message; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_message (
    id serial NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE webengine.auth_message OWNER TO webengine;

--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_message', 'id'), 1, false);


--
-- Name: auth_permission; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_permission (
    id serial NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE webengine.auth_permission OWNER TO webengine;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_permission', 'id'), 24, true);


--
-- Name: auth_user; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_user (
    id serial NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    "password" character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE webengine.auth_user OWNER TO webengine;

--
-- Name: auth_user_groups; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_user_groups (
    id serial NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE webengine.auth_user_groups OWNER TO webengine;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_user_groups', 'id'), 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_user', 'id'), 1, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE auth_user_user_permissions (
    id serial NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE webengine.auth_user_user_permissions OWNER TO webengine;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('auth_user_user_permissions', 'id'), 1, false);


--
-- Name: django_content_type; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE django_content_type (
    id serial NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE webengine.django_content_type OWNER TO webengine;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('django_content_type', 'id'), 8, true);


--
-- Name: django_session; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE webengine.django_session OWNER TO webengine;

--
-- Name: django_site; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE django_site (
    id serial NOT NULL,
    "domain" character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE webengine.django_site OWNER TO webengine;

--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('django_site', 'id'), 1, true);


--
-- Name: utils_usersetting; Type: TABLE; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE TABLE utils_usersetting (
    id serial NOT NULL,
    user_id integer NOT NULL,
    "key" character varying(128) NOT NULL,
    value character varying(512) NOT NULL
);


ALTER TABLE webengine.utils_usersetting OWNER TO webengine;

--
-- Name: utils_usersetting_id_seq; Type: SEQUENCE SET; Schema: webengine; Owner: webengine
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('utils_usersetting', 'id'), 1, true);


SET search_path = webengine, pg_catalog;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add user setting	8	add_usersetting
23	Can change user setting	8	change_usersetting
24	Can delete user setting	8	delete_usersetting
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_user (id, username, first_name, last_name, email, "password", is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
1	root			root-rxtx@smartjog.com	sha1$cc4f0$18cbe20e381833a9489734fa34118e37a67ba57c	t	t	t	2009-05-04 11:43:53.516356+02	2009-04-29 18:31:33.763924+02
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	user setting	utils	usersetting
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
8d1ca4af0f4d5e613ba145c4e41166c0	gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjYxZTk3MGJmMTVkNjg1NDliNGE4MTUzM2Y4\nOTBhNzMw\n	2009-05-18 14:04:00.759817+02
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY django_site (id, "domain", name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: utils_usersetting; Type: TABLE DATA; Schema: webengine; Owner: webengine
--

COPY utils_usersetting (id, user_id, "key", value) FROM stdin;
1	1	client_id	3
\.


SET search_path = webengine, pg_catalog;

--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: utils_usersetting_pkey; Type: CONSTRAINT; Schema: webengine; Owner: webengine; Tablespace:
--

ALTER TABLE ONLY utils_usersetting
    ADD CONSTRAINT utils_usersetting_pkey PRIMARY KEY (id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: utils_usersetting_user_id; Type: INDEX; Schema: webengine; Owner: webengine; Tablespace:
--

CREATE INDEX utils_usersetting_user_id ON utils_usersetting USING btree (user_id);


SET search_path = webengine, pg_catalog;

--
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: utils_usersetting_user_id_fkey; Type: FK CONSTRAINT; Schema: webengine; Owner: webengine
--

ALTER TABLE ONLY utils_usersetting
    ADD CONSTRAINT utils_usersetting_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--
