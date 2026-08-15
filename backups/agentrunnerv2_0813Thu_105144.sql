--
-- PostgreSQL database dump
--

\restrict Qmeys94vJnbCGNIpT1cPmzcHkxc6HpqCZlyIq8dnrdiiKgQ98au1y1dbG7ngu2U

-- Dumped from database version 17.9 (Debian 17.9-1.pgdg12+1)
-- Dumped by pg_dump version 17.9 (Debian 17.9-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: api_keys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_keys (
    id character varying(36) NOT NULL,
    key_hash text NOT NULL,
    key_prefix character varying(8) NOT NULL,
    name character varying(200) NOT NULL,
    role character varying(50) NOT NULL,
    created_by character varying(200) NOT NULL,
    expires_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    last_used_at timestamp without time zone
);


ALTER TABLE public.api_keys OWNER TO postgres;

--
-- Name: hosts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hosts (
    id character varying(36) NOT NULL,
    hostname character varying(200) NOT NULL,
    ip_address character varying(50),
    os_type character varying(20) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.hosts OWNER TO postgres;

--
-- Name: repo_workflow_assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repo_workflow_assignments (
    id character varying(36) NOT NULL,
    repo_id character varying(36) NOT NULL,
    workflow_name character varying(120) NOT NULL,
    display_name character varying(200),
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.repo_workflow_assignments OWNER TO postgres;

--
-- Name: repos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repos (
    id character varying(36) NOT NULL,
    name character varying(120) NOT NULL,
    path text NOT NULL,
    worker_id character varying(80) NOT NULL,
    worker_uuid character varying(36) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.repos OWNER TO postgres;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_id character varying(36) NOT NULL,
    email character varying(300) NOT NULL,
    role character varying(50) NOT NULL,
    is_system boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: user_workers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_workers (
    user_id character varying(36) NOT NULL,
    worker_id character varying(80) NOT NULL
);


ALTER TABLE public.user_workers OWNER TO postgres;

--
-- Name: worker_registry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.worker_registry (
    id character varying(36) NOT NULL,
    worker_id character varying(80) NOT NULL,
    host_id character varying(36),
    status character varying(30) NOT NULL,
    worker_label character varying(40) NOT NULL,
    is_enabled boolean NOT NULL,
    capabilities jsonb NOT NULL,
    current_run_id character varying(36),
    current_step_run_id character varying(36),
    last_heartbeat timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.worker_registry OWNER TO postgres;

--
-- Name: workflow_artifacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_artifacts (
    id character varying(36) NOT NULL,
    workflow_run_id character varying(36) NOT NULL,
    workflow_step_run_id character varying(36),
    artifact_key character varying(100) NOT NULL,
    role character varying(30) NOT NULL,
    file_path text NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_artifacts OWNER TO postgres;

--
-- Name: workflow_definitions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_definitions (
    id character varying(36) NOT NULL,
    name character varying(120) NOT NULL,
    job_prefix character varying(50) NOT NULL,
    init_step character varying(120),
    default_max_rejects integer NOT NULL,
    raw_definition jsonb NOT NULL,
    source_hash character varying(64) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_definitions OWNER TO postgres;

--
-- Name: workflow_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_events (
    id character varying(36) NOT NULL,
    workflow_run_id character varying(36) NOT NULL,
    workflow_step_run_id character varying(36),
    event_type character varying(60) NOT NULL,
    message text,
    payload jsonb NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_events OWNER TO postgres;

--
-- Name: workflow_reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_reviews (
    id character varying(36) NOT NULL,
    workflow_run_id character varying(36) NOT NULL,
    workflow_step_run_id character varying(36) NOT NULL,
    review_type character varying(50) NOT NULL,
    decision character varying(30) NOT NULL,
    remark text,
    findings jsonb,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_reviews OWNER TO postgres;

--
-- Name: workflow_runs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_runs (
    id character varying(36) NOT NULL,
    run_code character varying(80) NOT NULL,
    workflow_definition_id character varying(36) NOT NULL,
    run_status character varying(40) NOT NULL,
    action_requested character varying(40),
    action_feedback text,
    cancel_requested character varying(20),
    current_step_name character varying(120),
    current_step_run_id character varying(36),
    target_worker_id character varying(80),
    claimed_by_worker character varying(80),
    worker_label character varying(40) NOT NULL,
    project_root text,
    workspace_path text,
    job_dir text,
    input_payload jsonb NOT NULL,
    context_payload jsonb NOT NULL,
    error_message text,
    refine_iterations jsonb NOT NULL,
    submitted_at timestamp without time zone NOT NULL,
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_runs OWNER TO postgres;

--
-- Name: workflow_step_artifact_bindings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_step_artifact_bindings (
    id character varying(36) NOT NULL,
    step_definition_id character varying(36) NOT NULL,
    artifact_key character varying(100) NOT NULL,
    binding_type character varying(30) NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_step_artifact_bindings OWNER TO postgres;

--
-- Name: workflow_step_coder_policies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_step_coder_policies (
    id character varying(36) NOT NULL,
    step_definition_id character varying(36) NOT NULL,
    default_coder character varying(50),
    allowed_coders jsonb NOT NULL,
    must_differ boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_step_coder_policies OWNER TO postgres;

--
-- Name: workflow_step_definitions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_step_definitions (
    id character varying(36) NOT NULL,
    workflow_definition_id character varying(36) NOT NULL,
    step_name character varying(120) NOT NULL,
    step_order integer NOT NULL,
    execution_kind character varying(30) NOT NULL,
    prompt_file text,
    action character varying(100),
    requires_human_approval boolean NOT NULL,
    raw_config jsonb NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_step_definitions OWNER TO postgres;

--
-- Name: workflow_step_runs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_step_runs (
    id character varying(36) NOT NULL,
    workflow_run_id character varying(36) NOT NULL,
    step_name character varying(120) NOT NULL,
    sequence_no integer NOT NULL,
    attempt_no integer NOT NULL,
    step_status character varying(40) NOT NULL,
    step_outcome character varying(50),
    coder character varying(50),
    assigned_worker_id character varying(80),
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    duration_seconds integer,
    output_payload jsonb,
    usage_summary jsonb,
    error_message text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_step_runs OWNER TO postgres;

--
-- Name: workflow_step_transitions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_step_transitions (
    id character varying(36) NOT NULL,
    step_definition_id character varying(36) NOT NULL,
    transition_type character varying(50) NOT NULL,
    outcome character varying(50) NOT NULL,
    target_step_name character varying(120) NOT NULL,
    config jsonb NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.workflow_step_transitions OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
006
\.


--
-- Data for Name: api_keys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.api_keys (id, key_hash, key_prefix, name, role, created_by, expires_at, is_active, created_at, last_used_at) FROM stdin;
4ab3ca8d-1c5e-43bb-a756-be6598e423b1	$2b$12$AfX5HO18S.DZyhT0rAgBcexG6mmkoN7Vj1eq4sISikAk9P/.fjOl6	arb_far-	chua-worker-01	service-account	seed	\N	t	2026-08-13 02:38:06.42871	2026-08-13 02:40:49.663641
\.


--
-- Data for Name: hosts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hosts (id, hostname, ip_address, os_type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: repo_workflow_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.repo_workflow_assignments (id, repo_id, workflow_name, display_name, created_at) FROM stdin;
\.


--
-- Data for Name: repos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.repos (id, name, path, worker_id, worker_uuid, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_id, email, role, is_system, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_workers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_workers (user_id, worker_id) FROM stdin;
\.


--
-- Data for Name: worker_registry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.worker_registry (id, worker_id, host_id, status, worker_label, is_enabled, capabilities, current_run_id, current_step_run_id, last_heartbeat, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflow_artifacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_artifacts (id, workflow_run_id, workflow_step_run_id, artifact_key, role, file_path, created_at) FROM stdin;
\.


--
-- Data for Name: workflow_definitions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_definitions (id, name, job_prefix, init_step, default_max_rejects, raw_definition, source_hash, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflow_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_events (id, workflow_run_id, workflow_step_run_id, event_type, message, payload, created_at) FROM stdin;
\.


--
-- Data for Name: workflow_reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_reviews (id, workflow_run_id, workflow_step_run_id, review_type, decision, remark, findings, created_at) FROM stdin;
\.


--
-- Data for Name: workflow_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_runs (id, run_code, workflow_definition_id, run_status, action_requested, action_feedback, cancel_requested, current_step_name, current_step_run_id, target_worker_id, claimed_by_worker, worker_label, project_root, workspace_path, job_dir, input_payload, context_payload, error_message, refine_iterations, submitted_at, started_at, completed_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflow_step_artifact_bindings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_step_artifact_bindings (id, step_definition_id, artifact_key, binding_type, created_at) FROM stdin;
\.


--
-- Data for Name: workflow_step_coder_policies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_step_coder_policies (id, step_definition_id, default_coder, allowed_coders, must_differ, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflow_step_definitions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_step_definitions (id, workflow_definition_id, step_name, step_order, execution_kind, prompt_file, action, requires_human_approval, raw_config, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflow_step_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_step_runs (id, workflow_run_id, step_name, sequence_no, attempt_no, step_status, step_outcome, coder, assigned_worker_id, started_at, completed_at, duration_seconds, output_payload, usage_summary, error_message, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflow_step_transitions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_step_transitions (id, step_definition_id, transition_type, outcome, target_step_name, config, created_at) FROM stdin;
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: api_keys api_keys_key_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_key_hash_key UNIQUE (key_hash);


--
-- Name: api_keys api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_pkey PRIMARY KEY (id);


--
-- Name: hosts hosts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hosts
    ADD CONSTRAINT hosts_pkey PRIMARY KEY (id);


--
-- Name: repo_workflow_assignments repo_workflow_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repo_workflow_assignments
    ADD CONSTRAINT repo_workflow_assignments_pkey PRIMARY KEY (id);


--
-- Name: repos repos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repos
    ADD CONSTRAINT repos_pkey PRIMARY KEY (id);


--
-- Name: hosts uq_host_identity; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hosts
    ADD CONSTRAINT uq_host_identity UNIQUE (hostname, ip_address);


--
-- Name: repos uq_repo_name_worker; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repos
    ADD CONSTRAINT uq_repo_name_worker UNIQUE (name, worker_uuid);


--
-- Name: repo_workflow_assignments uq_repo_workflow; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repo_workflow_assignments
    ADD CONSTRAINT uq_repo_workflow UNIQUE (repo_id, workflow_name);


--
-- Name: workflow_step_definitions uq_workflow_step_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_definitions
    ADD CONSTRAINT uq_workflow_step_name UNIQUE (workflow_definition_id, step_name);


--
-- Name: workflow_step_definitions uq_workflow_step_order; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_definitions
    ADD CONSTRAINT uq_workflow_step_order UNIQUE (workflow_definition_id, step_order);


--
-- Name: user_roles user_roles_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_email_key UNIQUE (email);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id);


--
-- Name: user_workers user_workers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_workers
    ADD CONSTRAINT user_workers_pkey PRIMARY KEY (user_id, worker_id);


--
-- Name: worker_registry worker_registry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worker_registry
    ADD CONSTRAINT worker_registry_pkey PRIMARY KEY (id);


--
-- Name: workflow_artifacts workflow_artifacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_artifacts
    ADD CONSTRAINT workflow_artifacts_pkey PRIMARY KEY (id);


--
-- Name: workflow_definitions workflow_definitions_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_definitions
    ADD CONSTRAINT workflow_definitions_name_key UNIQUE (name);


--
-- Name: workflow_definitions workflow_definitions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_definitions
    ADD CONSTRAINT workflow_definitions_pkey PRIMARY KEY (id);


--
-- Name: workflow_events workflow_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_events
    ADD CONSTRAINT workflow_events_pkey PRIMARY KEY (id);


--
-- Name: workflow_reviews workflow_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviews
    ADD CONSTRAINT workflow_reviews_pkey PRIMARY KEY (id);


--
-- Name: workflow_runs workflow_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_runs
    ADD CONSTRAINT workflow_runs_pkey PRIMARY KEY (id);


--
-- Name: workflow_step_artifact_bindings workflow_step_artifact_bindings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_artifact_bindings
    ADD CONSTRAINT workflow_step_artifact_bindings_pkey PRIMARY KEY (id);


--
-- Name: workflow_step_coder_policies workflow_step_coder_policies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_coder_policies
    ADD CONSTRAINT workflow_step_coder_policies_pkey PRIMARY KEY (id);


--
-- Name: workflow_step_definitions workflow_step_definitions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_definitions
    ADD CONSTRAINT workflow_step_definitions_pkey PRIMARY KEY (id);


--
-- Name: workflow_step_runs workflow_step_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_runs
    ADD CONSTRAINT workflow_step_runs_pkey PRIMARY KEY (id);


--
-- Name: workflow_step_transitions workflow_step_transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_transitions
    ADD CONSTRAINT workflow_step_transitions_pkey PRIMARY KEY (id);


--
-- Name: ix_hosts_hostname; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_hosts_hostname ON public.hosts USING btree (hostname);


--
-- Name: ix_repo_workflow_assignments_repo_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_repo_workflow_assignments_repo_id ON public.repo_workflow_assignments USING btree (repo_id);


--
-- Name: ix_repos_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_repos_name ON public.repos USING btree (name);


--
-- Name: ix_repos_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_repos_worker_id ON public.repos USING btree (worker_id);


--
-- Name: ix_repos_worker_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_repos_worker_uuid ON public.repos USING btree (worker_uuid);


--
-- Name: ix_worker_registry_current_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_worker_registry_current_run_id ON public.worker_registry USING btree (current_run_id);


--
-- Name: ix_worker_registry_current_step_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_worker_registry_current_step_run_id ON public.worker_registry USING btree (current_step_run_id);


--
-- Name: ix_worker_registry_host_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_worker_registry_host_id ON public.worker_registry USING btree (host_id);


--
-- Name: ix_worker_registry_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_worker_registry_status ON public.worker_registry USING btree (status);


--
-- Name: ix_worker_registry_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_worker_registry_worker_id ON public.worker_registry USING btree (worker_id);


--
-- Name: ix_worker_registry_worker_label; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_worker_registry_worker_label ON public.worker_registry USING btree (worker_label);


--
-- Name: ix_workflow_artifacts_artifact_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_artifacts_artifact_key ON public.workflow_artifacts USING btree (artifact_key);


--
-- Name: ix_workflow_artifacts_workflow_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_artifacts_workflow_run_id ON public.workflow_artifacts USING btree (workflow_run_id);


--
-- Name: ix_workflow_artifacts_workflow_step_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_artifacts_workflow_step_run_id ON public.workflow_artifacts USING btree (workflow_step_run_id);


--
-- Name: ix_workflow_events_event_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_events_event_type ON public.workflow_events USING btree (event_type);


--
-- Name: ix_workflow_events_workflow_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_events_workflow_run_id ON public.workflow_events USING btree (workflow_run_id);


--
-- Name: ix_workflow_events_workflow_step_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_events_workflow_step_run_id ON public.workflow_events USING btree (workflow_step_run_id);


--
-- Name: ix_workflow_reviews_decision; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_reviews_decision ON public.workflow_reviews USING btree (decision);


--
-- Name: ix_workflow_reviews_workflow_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_reviews_workflow_run_id ON public.workflow_reviews USING btree (workflow_run_id);


--
-- Name: ix_workflow_reviews_workflow_step_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_reviews_workflow_step_run_id ON public.workflow_reviews USING btree (workflow_step_run_id);


--
-- Name: ix_workflow_runs_action_requested; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_runs_action_requested ON public.workflow_runs USING btree (action_requested);


--
-- Name: ix_workflow_runs_claimed_by_worker; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_runs_claimed_by_worker ON public.workflow_runs USING btree (claimed_by_worker);


--
-- Name: ix_workflow_runs_run_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_workflow_runs_run_code ON public.workflow_runs USING btree (run_code);


--
-- Name: ix_workflow_runs_run_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_runs_run_status ON public.workflow_runs USING btree (run_status);


--
-- Name: ix_workflow_runs_target_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_runs_target_worker_id ON public.workflow_runs USING btree (target_worker_id);


--
-- Name: ix_workflow_runs_worker_label; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_runs_worker_label ON public.workflow_runs USING btree (worker_label);


--
-- Name: ix_workflow_runs_workflow_definition_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_runs_workflow_definition_id ON public.workflow_runs USING btree (workflow_definition_id);


--
-- Name: ix_workflow_step_artifact_bindings_step_definition_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_artifact_bindings_step_definition_id ON public.workflow_step_artifact_bindings USING btree (step_definition_id);


--
-- Name: ix_workflow_step_coder_policies_step_definition_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_workflow_step_coder_policies_step_definition_id ON public.workflow_step_coder_policies USING btree (step_definition_id);


--
-- Name: ix_workflow_step_definitions_workflow_definition_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_definitions_workflow_definition_id ON public.workflow_step_definitions USING btree (workflow_definition_id);


--
-- Name: ix_workflow_step_runs_assigned_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_runs_assigned_worker_id ON public.workflow_step_runs USING btree (assigned_worker_id);


--
-- Name: ix_workflow_step_runs_step_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_runs_step_name ON public.workflow_step_runs USING btree (step_name);


--
-- Name: ix_workflow_step_runs_step_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_runs_step_status ON public.workflow_step_runs USING btree (step_status);


--
-- Name: ix_workflow_step_runs_workflow_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_runs_workflow_run_id ON public.workflow_step_runs USING btree (workflow_run_id);


--
-- Name: ix_workflow_step_transitions_step_definition_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_step_transitions_step_definition_id ON public.workflow_step_transitions USING btree (step_definition_id);


--
-- Name: repo_workflow_assignments repo_workflow_assignments_repo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repo_workflow_assignments
    ADD CONSTRAINT repo_workflow_assignments_repo_id_fkey FOREIGN KEY (repo_id) REFERENCES public.repos(id) ON DELETE CASCADE;


--
-- Name: repos repos_worker_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repos
    ADD CONSTRAINT repos_worker_uuid_fkey FOREIGN KEY (worker_uuid) REFERENCES public.worker_registry(id);


--
-- Name: user_workers user_workers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_workers
    ADD CONSTRAINT user_workers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_roles(user_id) ON DELETE CASCADE;


--
-- Name: worker_registry worker_registry_host_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worker_registry
    ADD CONSTRAINT worker_registry_host_id_fkey FOREIGN KEY (host_id) REFERENCES public.hosts(id);


--
-- Name: workflow_artifacts workflow_artifacts_workflow_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_artifacts
    ADD CONSTRAINT workflow_artifacts_workflow_run_id_fkey FOREIGN KEY (workflow_run_id) REFERENCES public.workflow_runs(id) ON DELETE CASCADE;


--
-- Name: workflow_artifacts workflow_artifacts_workflow_step_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_artifacts
    ADD CONSTRAINT workflow_artifacts_workflow_step_run_id_fkey FOREIGN KEY (workflow_step_run_id) REFERENCES public.workflow_step_runs(id) ON DELETE SET NULL;


--
-- Name: workflow_events workflow_events_workflow_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_events
    ADD CONSTRAINT workflow_events_workflow_run_id_fkey FOREIGN KEY (workflow_run_id) REFERENCES public.workflow_runs(id) ON DELETE CASCADE;


--
-- Name: workflow_events workflow_events_workflow_step_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_events
    ADD CONSTRAINT workflow_events_workflow_step_run_id_fkey FOREIGN KEY (workflow_step_run_id) REFERENCES public.workflow_step_runs(id) ON DELETE SET NULL;


--
-- Name: workflow_reviews workflow_reviews_workflow_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviews
    ADD CONSTRAINT workflow_reviews_workflow_run_id_fkey FOREIGN KEY (workflow_run_id) REFERENCES public.workflow_runs(id) ON DELETE CASCADE;


--
-- Name: workflow_reviews workflow_reviews_workflow_step_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviews
    ADD CONSTRAINT workflow_reviews_workflow_step_run_id_fkey FOREIGN KEY (workflow_step_run_id) REFERENCES public.workflow_step_runs(id) ON DELETE CASCADE;


--
-- Name: workflow_runs workflow_runs_workflow_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_runs
    ADD CONSTRAINT workflow_runs_workflow_definition_id_fkey FOREIGN KEY (workflow_definition_id) REFERENCES public.workflow_definitions(id) ON DELETE RESTRICT;


--
-- Name: workflow_step_artifact_bindings workflow_step_artifact_bindings_step_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_artifact_bindings
    ADD CONSTRAINT workflow_step_artifact_bindings_step_definition_id_fkey FOREIGN KEY (step_definition_id) REFERENCES public.workflow_step_definitions(id) ON DELETE CASCADE;


--
-- Name: workflow_step_coder_policies workflow_step_coder_policies_step_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_coder_policies
    ADD CONSTRAINT workflow_step_coder_policies_step_definition_id_fkey FOREIGN KEY (step_definition_id) REFERENCES public.workflow_step_definitions(id) ON DELETE CASCADE;


--
-- Name: workflow_step_definitions workflow_step_definitions_workflow_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_definitions
    ADD CONSTRAINT workflow_step_definitions_workflow_definition_id_fkey FOREIGN KEY (workflow_definition_id) REFERENCES public.workflow_definitions(id) ON DELETE CASCADE;


--
-- Name: workflow_step_runs workflow_step_runs_workflow_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_runs
    ADD CONSTRAINT workflow_step_runs_workflow_run_id_fkey FOREIGN KEY (workflow_run_id) REFERENCES public.workflow_runs(id) ON DELETE CASCADE;


--
-- Name: workflow_step_transitions workflow_step_transitions_step_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_step_transitions
    ADD CONSTRAINT workflow_step_transitions_step_definition_id_fkey FOREIGN KEY (step_definition_id) REFERENCES public.workflow_step_definitions(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Qmeys94vJnbCGNIpT1cPmzcHkxc6HpqCZlyIq8dnrdiiKgQ98au1y1dbG7ngu2U

