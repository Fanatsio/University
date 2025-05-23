PGDMP  :                    }            db_coursework    17.4    17.4 V    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16384    db_coursework    DATABASE     s   CREATE DATABASE db_coursework WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE db_coursework;
                     postgres    false            �            1259    16441    accessories    TABLE     A  CREATE TABLE public.accessories (
    accessories_id integer NOT NULL,
    accessories_name character varying(255),
    accessories_colour character varying(255),
    accessories_type character varying(255),
    accessories_quantity integer,
    provider_inn character varying(255),
    accessories_cost numeric(10,2)
);
    DROP TABLE public.accessories;
       public         heap r       postgres    false            �            1259    16440    accessories_accessories_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accessories_accessories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.accessories_accessories_id_seq;
       public               postgres    false    226            �           0    0    accessories_accessories_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.accessories_accessories_id_seq OWNED BY public.accessories.accessories_id;
          public               postgres    false    225            �            1259    16455 	   furniture    TABLE     =  CREATE TABLE public.furniture (
    furniture_id integer NOT NULL,
    furniture_colour character varying(255),
    furniture_article integer,
    id_material integer,
    furniture_type character varying(255),
    furniture_size numeric(5,2),
    furniture_name character varying(255),
    id_accessories integer
);
    DROP TABLE public.furniture;
       public         heap r       postgres    false            �            1259    16454    furniture_furniture_id_seq    SEQUENCE     �   CREATE SEQUENCE public.furniture_furniture_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.furniture_furniture_id_seq;
       public               postgres    false    228            �           0    0    furniture_furniture_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.furniture_furniture_id_seq OWNED BY public.furniture.furniture_id;
          public               postgres    false    227            �            1259    16401    legal_person    TABLE     5  CREATE TABLE public.legal_person (
    legal_person_id integer NOT NULL,
    legal_person_inn character varying(255),
    legal_person_name character varying(255),
    legal_person_phone character varying(255),
    legal_person_email character varying(255),
    legal_person_address character varying(255)
);
     DROP TABLE public.legal_person;
       public         heap r       postgres    false            �            1259    16400     legal_person_legal_person_id_seq    SEQUENCE     �   CREATE SEQUENCE public.legal_person_legal_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.legal_person_legal_person_id_seq;
       public               postgres    false    220            �           0    0     legal_person_legal_person_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.legal_person_legal_person_id_seq OWNED BY public.legal_person.legal_person_id;
          public               postgres    false    219            �            1259    16427    material    TABLE     ,  CREATE TABLE public.material (
    material_id integer NOT NULL,
    material_colour character varying(255),
    material_name character varying(255),
    material_type character varying(255),
    material_quantity integer,
    provider_inn character varying(255),
    material_cost numeric(10,2)
);
    DROP TABLE public.material;
       public         heap r       postgres    false            �            1259    16426    material_material_id_seq    SEQUENCE     �   CREATE SEQUENCE public.material_material_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.material_material_id_seq;
       public               postgres    false    224            �           0    0    material_material_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.material_material_id_seq OWNED BY public.material.material_id;
          public               postgres    false    223            �            1259    16386    natural_person    TABLE     9  CREATE TABLE public.natural_person (
    natural_person_id integer NOT NULL,
    natural_person_passport integer,
    natural_person_name character varying(255),
    natural_person_phone character varying(255),
    natural_person_email character varying(255),
    natural_person_address character varying(255)
);
 "   DROP TABLE public.natural_person;
       public         heap r       postgres    false            �            1259    16385 $   natural_person_natural_person_id_seq    SEQUENCE     �   CREATE SEQUENCE public.natural_person_natural_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.natural_person_natural_person_id_seq;
       public               postgres    false    218            �           0    0 $   natural_person_natural_person_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.natural_person_natural_person_id_seq OWNED BY public.natural_person.natural_person_id;
          public               postgres    false    217            �            1259    16476    orders    TABLE     �  CREATE TABLE public.orders (
    orders_id integer NOT NULL,
    orders_registration_date date,
    orders_total_cost numeric(10,2),
    order_number integer,
    category_customer character varying(50),
    orders_status character varying(255),
    customer_id integer,
    CONSTRAINT check_customer_id CHECK (((((category_customer)::text = 'Юр. лицо'::text) AND (customer_id IS NOT NULL)) OR (((category_customer)::text = 'Физ. лицо'::text) AND (customer_id IS NOT NULL)))),
    CONSTRAINT orders_category_customer_check CHECK (((category_customer)::text = ANY ((ARRAY['Юр. лицо'::character varying, 'Физ. лицо'::character varying])::text[])))
);
    DROP TABLE public.orders;
       public         heap r       postgres    false            �            1259    16475    orders_orders_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.orders_orders_id_seq;
       public               postgres    false    230            �           0    0    orders_orders_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.orders_orders_id_seq OWNED BY public.orders.orders_id;
          public               postgres    false    229            �            1259    16416    provider    TABLE     �   CREATE TABLE public.provider (
    provider_id integer NOT NULL,
    provider_inn character varying(255),
    provider_name character varying(255),
    provider_address character varying(255)
);
    DROP TABLE public.provider;
       public         heap r       postgres    false            �            1259    16415    provider_provider_id_seq    SEQUENCE     �   CREATE SEQUENCE public.provider_provider_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.provider_provider_id_seq;
       public               postgres    false    222            �           0    0    provider_provider_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.provider_provider_id_seq OWNED BY public.provider.provider_id;
          public               postgres    false    221            �            1259    16516    users    TABLE     �   CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    16515    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public               postgres    false    234            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public               postgres    false    233            �            1259    16497    waybill    TABLE     �   CREATE TABLE public.waybill (
    waybill_id integer NOT NULL,
    waybill_number integer,
    article_furniture integer,
    furniture_quantity integer,
    orders_number integer
);
    DROP TABLE public.waybill;
       public         heap r       postgres    false            �            1259    16496    waybill_waybill_id_seq    SEQUENCE     �   CREATE SEQUENCE public.waybill_waybill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.waybill_waybill_id_seq;
       public               postgres    false    232            �           0    0    waybill_waybill_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.waybill_waybill_id_seq OWNED BY public.waybill.waybill_id;
          public               postgres    false    231            �           2604    16444    accessories accessories_id    DEFAULT     �   ALTER TABLE ONLY public.accessories ALTER COLUMN accessories_id SET DEFAULT nextval('public.accessories_accessories_id_seq'::regclass);
 I   ALTER TABLE public.accessories ALTER COLUMN accessories_id DROP DEFAULT;
       public               postgres    false    225    226    226            �           2604    16458    furniture furniture_id    DEFAULT     �   ALTER TABLE ONLY public.furniture ALTER COLUMN furniture_id SET DEFAULT nextval('public.furniture_furniture_id_seq'::regclass);
 E   ALTER TABLE public.furniture ALTER COLUMN furniture_id DROP DEFAULT;
       public               postgres    false    228    227    228            �           2604    16404    legal_person legal_person_id    DEFAULT     �   ALTER TABLE ONLY public.legal_person ALTER COLUMN legal_person_id SET DEFAULT nextval('public.legal_person_legal_person_id_seq'::regclass);
 K   ALTER TABLE public.legal_person ALTER COLUMN legal_person_id DROP DEFAULT;
       public               postgres    false    219    220    220            �           2604    16430    material material_id    DEFAULT     |   ALTER TABLE ONLY public.material ALTER COLUMN material_id SET DEFAULT nextval('public.material_material_id_seq'::regclass);
 C   ALTER TABLE public.material ALTER COLUMN material_id DROP DEFAULT;
       public               postgres    false    224    223    224            �           2604    16389     natural_person natural_person_id    DEFAULT     �   ALTER TABLE ONLY public.natural_person ALTER COLUMN natural_person_id SET DEFAULT nextval('public.natural_person_natural_person_id_seq'::regclass);
 O   ALTER TABLE public.natural_person ALTER COLUMN natural_person_id DROP DEFAULT;
       public               postgres    false    218    217    218            �           2604    16479    orders orders_id    DEFAULT     t   ALTER TABLE ONLY public.orders ALTER COLUMN orders_id SET DEFAULT nextval('public.orders_orders_id_seq'::regclass);
 ?   ALTER TABLE public.orders ALTER COLUMN orders_id DROP DEFAULT;
       public               postgres    false    230    229    230            �           2604    16419    provider provider_id    DEFAULT     |   ALTER TABLE ONLY public.provider ALTER COLUMN provider_id SET DEFAULT nextval('public.provider_provider_id_seq'::regclass);
 C   ALTER TABLE public.provider ALTER COLUMN provider_id DROP DEFAULT;
       public               postgres    false    221    222    222            �           2604    16519    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public               postgres    false    234    233    234            �           2604    16500    waybill waybill_id    DEFAULT     x   ALTER TABLE ONLY public.waybill ALTER COLUMN waybill_id SET DEFAULT nextval('public.waybill_waybill_id_seq'::regclass);
 A   ALTER TABLE public.waybill ALTER COLUMN waybill_id DROP DEFAULT;
       public               postgres    false    231    232    232            �          0    16441    accessories 
   TABLE DATA           �   COPY public.accessories (accessories_id, accessories_name, accessories_colour, accessories_type, accessories_quantity, provider_inn, accessories_cost) FROM stdin;
    public               postgres    false    226   �q       �          0    16455 	   furniture 
   TABLE DATA           �   COPY public.furniture (furniture_id, furniture_colour, furniture_article, id_material, furniture_type, furniture_size, furniture_name, id_accessories) FROM stdin;
    public               postgres    false    228   �r       }          0    16401    legal_person 
   TABLE DATA           �   COPY public.legal_person (legal_person_id, legal_person_inn, legal_person_name, legal_person_phone, legal_person_email, legal_person_address) FROM stdin;
    public               postgres    false    220   �s       �          0    16427    material 
   TABLE DATA           �   COPY public.material (material_id, material_colour, material_name, material_type, material_quantity, provider_inn, material_cost) FROM stdin;
    public               postgres    false    224   tu       {          0    16386    natural_person 
   TABLE DATA           �   COPY public.natural_person (natural_person_id, natural_person_passport, natural_person_name, natural_person_phone, natural_person_email, natural_person_address) FROM stdin;
    public               postgres    false    218   Xv       �          0    16476    orders 
   TABLE DATA           �   COPY public.orders (orders_id, orders_registration_date, orders_total_cost, order_number, category_customer, orders_status, customer_id) FROM stdin;
    public               postgres    false    230   x                 0    16416    provider 
   TABLE DATA           ^   COPY public.provider (provider_id, provider_inn, provider_name, provider_address) FROM stdin;
    public               postgres    false    222   �x       �          0    16516    users 
   TABLE DATA           <   COPY public.users (user_id, username, password) FROM stdin;
    public               postgres    false    234   z       �          0    16497    waybill 
   TABLE DATA           s   COPY public.waybill (waybill_id, waybill_number, article_furniture, furniture_quantity, orders_number) FROM stdin;
    public               postgres    false    232   ,z       �           0    0    accessories_accessories_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.accessories_accessories_id_seq', 5, true);
          public               postgres    false    225            �           0    0    furniture_furniture_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.furniture_furniture_id_seq', 5, true);
          public               postgres    false    227            �           0    0     legal_person_legal_person_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.legal_person_legal_person_id_seq', 5, true);
          public               postgres    false    219            �           0    0    material_material_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.material_material_id_seq', 5, true);
          public               postgres    false    223            �           0    0 $   natural_person_natural_person_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.natural_person_natural_person_id_seq', 5, true);
          public               postgres    false    217            �           0    0    orders_orders_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_orders_id_seq', 8, true);
          public               postgres    false    229            �           0    0    provider_provider_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.provider_provider_id_seq', 5, true);
          public               postgres    false    221            �           0    0    users_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);
          public               postgres    false    233            �           0    0    waybill_waybill_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.waybill_waybill_id_seq', 6, true);
          public               postgres    false    231            �           2606    16448    accessories accessories_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.accessories
    ADD CONSTRAINT accessories_pkey PRIMARY KEY (accessories_id);
 F   ALTER TABLE ONLY public.accessories DROP CONSTRAINT accessories_pkey;
       public                 postgres    false    226            �           2606    16464 )   furniture furniture_furniture_article_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.furniture
    ADD CONSTRAINT furniture_furniture_article_key UNIQUE (furniture_article);
 S   ALTER TABLE ONLY public.furniture DROP CONSTRAINT furniture_furniture_article_key;
       public                 postgres    false    228            �           2606    16462    furniture furniture_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.furniture
    ADD CONSTRAINT furniture_pkey PRIMARY KEY (furniture_id);
 B   ALTER TABLE ONLY public.furniture DROP CONSTRAINT furniture_pkey;
       public                 postgres    false    228            �           2606    16414 0   legal_person legal_person_legal_person_email_key 
   CONSTRAINT     y   ALTER TABLE ONLY public.legal_person
    ADD CONSTRAINT legal_person_legal_person_email_key UNIQUE (legal_person_email);
 Z   ALTER TABLE ONLY public.legal_person DROP CONSTRAINT legal_person_legal_person_email_key;
       public                 postgres    false    220            �           2606    16410 .   legal_person legal_person_legal_person_inn_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.legal_person
    ADD CONSTRAINT legal_person_legal_person_inn_key UNIQUE (legal_person_inn);
 X   ALTER TABLE ONLY public.legal_person DROP CONSTRAINT legal_person_legal_person_inn_key;
       public                 postgres    false    220            �           2606    16412 0   legal_person legal_person_legal_person_phone_key 
   CONSTRAINT     y   ALTER TABLE ONLY public.legal_person
    ADD CONSTRAINT legal_person_legal_person_phone_key UNIQUE (legal_person_phone);
 Z   ALTER TABLE ONLY public.legal_person DROP CONSTRAINT legal_person_legal_person_phone_key;
       public                 postgres    false    220            �           2606    16408    legal_person legal_person_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.legal_person
    ADD CONSTRAINT legal_person_pkey PRIMARY KEY (legal_person_id);
 H   ALTER TABLE ONLY public.legal_person DROP CONSTRAINT legal_person_pkey;
       public                 postgres    false    220            �           2606    16434    material material_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.material
    ADD CONSTRAINT material_pkey PRIMARY KEY (material_id);
 @   ALTER TABLE ONLY public.material DROP CONSTRAINT material_pkey;
       public                 postgres    false    224            �           2606    16399 6   natural_person natural_person_natural_person_email_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.natural_person
    ADD CONSTRAINT natural_person_natural_person_email_key UNIQUE (natural_person_email);
 `   ALTER TABLE ONLY public.natural_person DROP CONSTRAINT natural_person_natural_person_email_key;
       public                 postgres    false    218            �           2606    16395 9   natural_person natural_person_natural_person_passport_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.natural_person
    ADD CONSTRAINT natural_person_natural_person_passport_key UNIQUE (natural_person_passport);
 c   ALTER TABLE ONLY public.natural_person DROP CONSTRAINT natural_person_natural_person_passport_key;
       public                 postgres    false    218            �           2606    16397 6   natural_person natural_person_natural_person_phone_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.natural_person
    ADD CONSTRAINT natural_person_natural_person_phone_key UNIQUE (natural_person_phone);
 `   ALTER TABLE ONLY public.natural_person DROP CONSTRAINT natural_person_natural_person_phone_key;
       public                 postgres    false    218            �           2606    16393 "   natural_person natural_person_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.natural_person
    ADD CONSTRAINT natural_person_pkey PRIMARY KEY (natural_person_id);
 L   ALTER TABLE ONLY public.natural_person DROP CONSTRAINT natural_person_pkey;
       public                 postgres    false    218            �           2606    16485    orders orders_order_number_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_order_number_key UNIQUE (order_number);
 H   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_order_number_key;
       public                 postgres    false    230            �           2606    16483    orders orders_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (orders_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    230            �           2606    16423    provider provider_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.provider
    ADD CONSTRAINT provider_pkey PRIMARY KEY (provider_id);
 @   ALTER TABLE ONLY public.provider DROP CONSTRAINT provider_pkey;
       public                 postgres    false    222            �           2606    16425 "   provider provider_provider_inn_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.provider
    ADD CONSTRAINT provider_provider_inn_key UNIQUE (provider_inn);
 L   ALTER TABLE ONLY public.provider DROP CONSTRAINT provider_provider_inn_key;
       public                 postgres    false    222            �           2606    16521    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    234            �           2606    16523    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    234            �           2606    16502    waybill waybill_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.waybill
    ADD CONSTRAINT waybill_pkey PRIMARY KEY (waybill_id);
 >   ALTER TABLE ONLY public.waybill DROP CONSTRAINT waybill_pkey;
       public                 postgres    false    232            �           2606    16504 "   waybill waybill_waybill_number_key 
   CONSTRAINT     g   ALTER TABLE ONLY public.waybill
    ADD CONSTRAINT waybill_waybill_number_key UNIQUE (waybill_number);
 L   ALTER TABLE ONLY public.waybill DROP CONSTRAINT waybill_waybill_number_key;
       public                 postgres    false    232            �           2606    16449 )   accessories accessories_provider_inn_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.accessories
    ADD CONSTRAINT accessories_provider_inn_fkey FOREIGN KEY (provider_inn) REFERENCES public.provider(provider_inn);
 S   ALTER TABLE ONLY public.accessories DROP CONSTRAINT accessories_provider_inn_fkey;
       public               postgres    false    226    222    4812            �           2606    16486    orders fk_legal_person    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_legal_person FOREIGN KEY (customer_id) REFERENCES public.legal_person(legal_person_id) DEFERRABLE INITIALLY DEFERRED;
 @   ALTER TABLE ONLY public.orders DROP CONSTRAINT fk_legal_person;
       public               postgres    false    220    230    4808            �           2606    16491    orders fk_natural_person    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_natural_person FOREIGN KEY (customer_id) REFERENCES public.natural_person(natural_person_id) DEFERRABLE INITIALLY DEFERRED;
 B   ALTER TABLE ONLY public.orders DROP CONSTRAINT fk_natural_person;
       public               postgres    false    4800    230    218            �           2606    16470 '   furniture furniture_id_accessories_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.furniture
    ADD CONSTRAINT furniture_id_accessories_fkey FOREIGN KEY (id_accessories) REFERENCES public.accessories(accessories_id);
 Q   ALTER TABLE ONLY public.furniture DROP CONSTRAINT furniture_id_accessories_fkey;
       public               postgres    false    226    228    4816            �           2606    16465 $   furniture furniture_id_material_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.furniture
    ADD CONSTRAINT furniture_id_material_fkey FOREIGN KEY (id_material) REFERENCES public.material(material_id);
 N   ALTER TABLE ONLY public.furniture DROP CONSTRAINT furniture_id_material_fkey;
       public               postgres    false    4814    228    224            �           2606    16435 #   material material_provider_inn_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.material
    ADD CONSTRAINT material_provider_inn_fkey FOREIGN KEY (provider_inn) REFERENCES public.provider(provider_inn);
 M   ALTER TABLE ONLY public.material DROP CONSTRAINT material_provider_inn_fkey;
       public               postgres    false    4812    222    224            �           2606    16505 &   waybill waybill_article_furniture_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.waybill
    ADD CONSTRAINT waybill_article_furniture_fkey FOREIGN KEY (article_furniture) REFERENCES public.furniture(furniture_article);
 P   ALTER TABLE ONLY public.waybill DROP CONSTRAINT waybill_article_furniture_fkey;
       public               postgres    false    232    4818    228            �           2606    16510 "   waybill waybill_orders_number_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.waybill
    ADD CONSTRAINT waybill_orders_number_fkey FOREIGN KEY (orders_number) REFERENCES public.orders(order_number);
 L   ALTER TABLE ONLY public.waybill DROP CONSTRAINT waybill_orders_number_fkey;
       public               postgres    false    4822    232    230            �   �   x�m�MN�@��� #�g��.&�BQ�X!�TlSh В^��F�I�"$6+�|yq"x����͑���F#XY�r'xf��7:�U#����N��y&I�>�K�hm��-'�ohm���ږ�{t|ղ񟚆?�4�T]�5��	�F�.�P+��>w��)'�სS&��ʃ�J]���_'[�ٜ;�y�؍9_�1�(?`�����4��`��g��v\Ԁr�X	n�y���Ĕ�)�RH~�4�Dݱw�� ��      �   �   x�U�KN�@D�=��`͌mw�0��],E|VA"ʎ�	��qH�B���&`��j�_WM<�oC����\R
EF}��c����|��z]JtIp���.p0P:m8r�HP����:Ֆ�L�ɖ<^tn�$W
�_ޑV
�/����F[I���z�ՙNy�c���N�K*���Y'�)+���LVQn.}G��>���3��6R�����qj�Zq;d'����kx���ﱗ��ι/����      }   �  x����N�P�קOѽH,mi�� nK$�M�,p�E#�.4�� �P�=����#��ʜ��t:����!�Ȉ��w����F��3�&͹A?:u�J���J�+�eP�yɼw�墅��r��Ѐz�k4����2- #��!WPj��s�?DtFC�	�ݐ�У$iA1�kT-sU�'�
w��&D��g�B�<��K=ԝp��:4B������{i���t%fk����L��{T[��S�������3�l�K���"y��%@���r�xȷ8UT���,a[{���U�*��
� ��.q�5N�"�
Y��<��"z�~�&b�!d����s}�
���ؚ-�};Z�K���ٺ6|��DNjc�y�*u�uW6���+�v�4�k�qn      �   �   x�UPKn�@]{N�	"��$ܥ�	�A�j�]+�J` E
�p���M�H�,f�����O���?8�pC�&��3�'����������J��mj�J�[�L5�w���+��o�WI}��4����Ma�1��#��^�5{{�*u�ȯM��B%콛e�����H��VZ�`A�R��7c��ȹ8�L|��s�|�+m^�%!����      {   �  x�]��N�@��ۧ�]l��.�7�K#��A�
D���?1� B�W�}#gZZ�i�n�������i��Sv����;��p[X�Fw�6����C��H߲#�%ιR�Z۫m�k�T}�va�>��p�2����2�S�Xa��
&,,���K,!���EvPnj�;l� >i8���K|���8�S.�.kT[�A۳�f�e�k�{�Ir�1�}JB�"ܘc��1���qa��S^<_��ڋ3�̑������RڶR�Y��g��<���"����(6$����gR��!	C\�½K}�Zah�?�8@)��9�u�����S���$�o����zjf3"!G�%��Ҧ��PrCe�2�T|�X{�/L�ň����^-��5�T	��|��A�/�8�M+ڨ����%�D�ϲqj���R��      �   �   x�m�A�0E��Spȴ��w�0�;�ލk�H�+��ȉ1)�n'y��W�a�R��f�3g�rcM�b�3K0b�̄�?�YzL��	�!m�!�|�G'���F����^6(�U0�H�E��w�"z��v�II�r�䫎�<�G#��ǻ�Wd3\�bC�*�cC�Z4������R��̱y           x�e�aN�@�Ϟ�T��zSh�?����(ڴ� �B�E�
oo��mJ�&dv���f�P�4�������{<��6�f�?�=�G�QN<�@�{xF�{��UJ�8�P�ZE��F����Z��lt8��
k���3~��J*�2�3�X�Y2w65�$�����dA���
�\��T72<����VZŢ�է#thآ�J����d�w��n�vT�����[Lg�X�I�xE����"��`K&��pp���r�[�н��"�n|���$�      �      x�3�LL����44261����� /�      �   E   x�%�� 0г�T�L���h�1/�����1� E�("B��V E)z�(Q�մ
-��[�� \=J�     