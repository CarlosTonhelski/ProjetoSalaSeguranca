--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2026-05-12 16:03:44

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 17976)
-- Name: administradores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.administradores (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    senha character varying(255) NOT NULL
);


ALTER TABLE public.administradores OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17975)
-- Name: administradores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.administradores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.administradores_id_seq OWNER TO postgres;

--
-- TOC entry 4873 (class 0 OID 0)
-- Dependencies: 219
-- Name: administradores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.administradores_id_seq OWNED BY public.administradores.id;


--
-- TOC entry 216 (class 1259 OID 17946)
-- Name: colaboradores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.colaboradores (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    matricula character varying(20) NOT NULL,
    rfid_tag character varying(50) NOT NULL,
    cargo character varying(50) NOT NULL,
    acesso_permitido boolean DEFAULT false NOT NULL,
    ativo boolean DEFAULT true NOT NULL,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.colaboradores OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 17945)
-- Name: colaboradores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.colaboradores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.colaboradores_id_seq OWNER TO postgres;

--
-- TOC entry 4874 (class 0 OID 0)
-- Dependencies: 215
-- Name: colaboradores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.colaboradores_id_seq OWNED BY public.colaboradores.id;


--
-- TOC entry 218 (class 1259 OID 17960)
-- Name: logs_acesso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs_acesso (
    id integer NOT NULL,
    colaborador_id integer,
    nome_tag_nao_cadastrada character varying(100),
    rfid_tag_lida character varying(50) NOT NULL,
    tipo_evento character varying(20) NOT NULL,
    data_hora timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    observacao text,
    dispositivo_origem character varying(100) DEFAULT 'Raspberry Pi Sala AAA'::character varying
);


ALTER TABLE public.logs_acesso OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17959)
-- Name: logs_acesso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_acesso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_acesso_id_seq OWNER TO postgres;

--
-- TOC entry 4875 (class 0 OID 0)
-- Dependencies: 217
-- Name: logs_acesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_acesso_id_seq OWNED BY public.logs_acesso.id;


--
-- TOC entry 4705 (class 2604 OID 17979)
-- Name: administradores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administradores ALTER COLUMN id SET DEFAULT nextval('public.administradores_id_seq'::regclass);


--
-- TOC entry 4698 (class 2604 OID 17949)
-- Name: colaboradores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colaboradores ALTER COLUMN id SET DEFAULT nextval('public.colaboradores_id_seq'::regclass);


--
-- TOC entry 4702 (class 2604 OID 17963)
-- Name: logs_acesso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso ALTER COLUMN id SET DEFAULT nextval('public.logs_acesso_id_seq'::regclass);


--
-- TOC entry 4867 (class 0 OID 17976)
-- Dependencies: 220
-- Data for Name: administradores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administradores (id, username, senha) FROM stdin;
1	admin	admin123
\.


--
-- TOC entry 4863 (class 0 OID 17946)
-- Dependencies: 216
-- Data for Name: colaboradores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.colaboradores (id, nome, matricula, rfid_tag, cargo, acesso_permitido, ativo, criado_em) FROM stdin;
4	Maria	2026004	TAG004	RH	f	t	2026-05-11 20:04:31.692356
1	Joao	1136868	TAG001	Game Designer	t	t	2026-05-11 20:04:31.692356
2	Carlos	1137093	TAG002	Concept Artist	t	t	2026-05-11 20:04:31.692356
3	Julia	1136562	TAG003	Estagiaria	f	t	2026-05-11 20:04:31.692356
\.


--
-- TOC entry 4865 (class 0 OID 17960)
-- Dependencies: 218
-- Data for Name: logs_acesso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs_acesso (id, colaborador_id, nome_tag_nao_cadastrada, rfid_tag_lida, tipo_evento, data_hora, observacao, dispositivo_origem) FROM stdin;
1	1	\N	TAG001	ENTRADA	2026-05-11 20:05:05.216052	Entrada autorizada	Raspberry Pi Sala AAA
2	1	\N	TAG001	SAIDA	2026-05-11 20:05:05.216052	Saida registrada	Raspberry Pi Sala AAA
3	2	\N	TAG002	ENTRADA	2026-05-11 20:05:05.216052	Entrada autorizada	Raspberry Pi Sala AAA
4	3	\N	TAG003	NEGADO	2026-05-11 20:05:05.216052	Colaborador sem permissao	Raspberry Pi Sala AAA
5	4	\N	TAG004	NEGADO	2026-05-11 20:05:05.216052	Colaborador sem permissao	Raspberry Pi Sala AAA
6	\N	Alisson	TAG005	INVASAO	2026-05-11 20:05:05.216052	Tentativa de invasao com tag desconhecida	Raspberry Pi Sala AAA
7	\N	Desconhecido	TAG006	INVASAO	2026-05-11 20:05:05.216052	RFID nao cadastrada	Raspberry Pi Sala AAA
8	1	\N	TAG001	ENTRADA	2026-05-12 16:13:42.307319	Entrada autorizada	Raspberry Pi Sala AAA
9	1	\N	TAG001	SAIDA	2026-05-12 16:14:43.90931	Saida registrada	Raspberry Pi Sala AAA
10	1	\N	TAG001	ENTRADA	2026-05-12 16:24:50.455731	Entrada autorizada	Raspberry Pi Sala AAA
11	1	\N	TAG001	SAIDA	2026-05-12 16:25:49.274149	Saida registrada	Raspberry Pi Sala AAA
12	\N	Desconhecido	TAG999	INVASAO	2026-05-12 17:18:16.255963	RFID nao cadastrada	Raspberry Pi Sala AAA
\.


--
-- TOC entry 4876 (class 0 OID 0)
-- Dependencies: 219
-- Name: administradores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administradores_id_seq', 1, true);


--
-- TOC entry 4877 (class 0 OID 0)
-- Dependencies: 215
-- Name: colaboradores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.colaboradores_id_seq', 7, true);


--
-- TOC entry 4878 (class 0 OID 0)
-- Dependencies: 217
-- Name: logs_acesso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_acesso_id_seq', 12, true);


--
-- TOC entry 4715 (class 2606 OID 17981)
-- Name: administradores administradores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administradores
    ADD CONSTRAINT administradores_pkey PRIMARY KEY (id);


--
-- TOC entry 4717 (class 2606 OID 17983)
-- Name: administradores administradores_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administradores
    ADD CONSTRAINT administradores_username_key UNIQUE (username);


--
-- TOC entry 4707 (class 2606 OID 17956)
-- Name: colaboradores colaboradores_matricula_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT colaboradores_matricula_key UNIQUE (matricula);


--
-- TOC entry 4709 (class 2606 OID 17954)
-- Name: colaboradores colaboradores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT colaboradores_pkey PRIMARY KEY (id);


--
-- TOC entry 4711 (class 2606 OID 17958)
-- Name: colaboradores colaboradores_rfid_tag_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT colaboradores_rfid_tag_key UNIQUE (rfid_tag);


--
-- TOC entry 4713 (class 2606 OID 17969)
-- Name: logs_acesso logs_acesso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso
    ADD CONSTRAINT logs_acesso_pkey PRIMARY KEY (id);


--
-- TOC entry 4718 (class 2606 OID 17970)
-- Name: logs_acesso fk_colaborador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso
    ADD CONSTRAINT fk_colaborador FOREIGN KEY (colaborador_id) REFERENCES public.colaboradores(id) ON DELETE SET NULL;


-- Completed on 2026-05-12 16:03:45

--
-- PostgreSQL database dump complete
--

