PGDMP                       }            SecuritySystem    17.4    17.4     A           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            B           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            C           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            D           1262    16524    SecuritySystem    DATABASE     v   CREATE DATABASE "SecuritySystem" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
     DROP DATABASE "SecuritySystem";
                     postgres    false            R           1247    16578    checkpoint_type    TYPE     \   CREATE TYPE public.checkpoint_type AS ENUM (
    'entry',
    'exit',
    'intermediate'
);
 "   DROP TYPE public.checkpoint_type;
       public               postgres    false            �            1259    16712 
   checkpoint    TABLE     �   CREATE TABLE public.checkpoint (
    id integer NOT NULL,
    hazardous_area_id integer NOT NULL,
    coordinates text NOT NULL,
    type public.checkpoint_type NOT NULL
);
    DROP TABLE public.checkpoint;
       public         heap r       postgres    false    850            �            1259    16698    employee    TABLE     �   CREATE TABLE public.employee (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    rfid_tag character varying(50) NOT NULL
);
    DROP TABLE public.employee;
       public         heap r       postgres    false            �            1259    16705    hazardous_area    TABLE     �   CREATE TABLE public.hazardous_area (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    coordinates text NOT NULL
);
 "   DROP TABLE public.hazardous_area;
       public         heap r       postgres    false            �            1259    16724    monitoring_session    TABLE     =  CREATE TABLE public.monitoring_session (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    hazardous_area_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone,
    violations_count integer DEFAULT 0,
    report_link character varying(255)
);
 &   DROP TABLE public.monitoring_session;
       public         heap r       postgres    false            �            1259    16740    notification    TABLE     �   CREATE TABLE public.notification (
    id integer NOT NULL,
    monitoring_session_id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    violation_type character varying(50) NOT NULL,
    description text
);
     DROP TABLE public.notification;
       public         heap r       postgres    false            <          0    16712 
   checkpoint 
   TABLE DATA           N   COPY public.checkpoint (id, hazardous_area_id, coordinates, type) FROM stdin;
    public               postgres    false    219   �       :          0    16698    employee 
   TABLE DATA           6   COPY public.employee (id, name, rfid_tag) FROM stdin;
    public               postgres    false    217   �       ;          0    16705    hazardous_area 
   TABLE DATA           ?   COPY public.hazardous_area (id, name, coordinates) FROM stdin;
    public               postgres    false    218   �       =          0    16724    monitoring_session 
   TABLE DATA           �   COPY public.monitoring_session (id, employee_id, hazardous_area_id, start_time, end_time, violations_count, report_link) FROM stdin;
    public               postgres    false    220           >          0    16740    notification 
   TABLE DATA           k   COPY public.notification (id, monitoring_session_id, "timestamp", violation_type, description) FROM stdin;
    public               postgres    false    221   "        �           2606    16718    checkpoint checkpoint_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.checkpoint
    ADD CONSTRAINT checkpoint_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.checkpoint DROP CONSTRAINT checkpoint_pkey;
       public                 postgres    false    219            �           2606    16702    employee employee_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.employee DROP CONSTRAINT employee_pkey;
       public                 postgres    false    217            �           2606    16704    employee employee_rfid_tag_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_rfid_tag_key UNIQUE (rfid_tag);
 H   ALTER TABLE ONLY public.employee DROP CONSTRAINT employee_rfid_tag_key;
       public                 postgres    false    217            �           2606    16711 "   hazardous_area hazardous_area_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.hazardous_area
    ADD CONSTRAINT hazardous_area_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.hazardous_area DROP CONSTRAINT hazardous_area_pkey;
       public                 postgres    false    218            �           2606    16729 *   monitoring_session monitoring_session_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.monitoring_session
    ADD CONSTRAINT monitoring_session_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.monitoring_session DROP CONSTRAINT monitoring_session_pkey;
       public                 postgres    false    220            �           2606    16746    notification notification_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.notification DROP CONSTRAINT notification_pkey;
       public                 postgres    false    221            �           2606    16719 ,   checkpoint checkpoint_hazardous_area_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.checkpoint
    ADD CONSTRAINT checkpoint_hazardous_area_id_fkey FOREIGN KEY (hazardous_area_id) REFERENCES public.hazardous_area(id);
 V   ALTER TABLE ONLY public.checkpoint DROP CONSTRAINT checkpoint_hazardous_area_id_fkey;
       public               postgres    false    4766    219    218            �           2606    16730 6   monitoring_session monitoring_session_employee_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.monitoring_session
    ADD CONSTRAINT monitoring_session_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id);
 `   ALTER TABLE ONLY public.monitoring_session DROP CONSTRAINT monitoring_session_employee_id_fkey;
       public               postgres    false    4762    217    220            �           2606    16735 <   monitoring_session monitoring_session_hazardous_area_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.monitoring_session
    ADD CONSTRAINT monitoring_session_hazardous_area_id_fkey FOREIGN KEY (hazardous_area_id) REFERENCES public.hazardous_area(id);
 f   ALTER TABLE ONLY public.monitoring_session DROP CONSTRAINT monitoring_session_hazardous_area_id_fkey;
       public               postgres    false    4766    218    220            �           2606    16747 4   notification notification_monitoring_session_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_monitoring_session_id_fkey FOREIGN KEY (monitoring_session_id) REFERENCES public.monitoring_session(id);
 ^   ALTER TABLE ONLY public.notification DROP CONSTRAINT notification_monitoring_session_id_fkey;
       public               postgres    false    221    220    4770            <      x������ � �      :      x������ � �      ;      x������ � �      =      x������ � �      >      x������ � �     