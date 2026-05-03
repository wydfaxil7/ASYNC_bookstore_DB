--
-- PostgreSQL database dump
--

\restrict xTGOjMEbXzoDQJbnaQvpTr1CGPhs2uGz6g7eTOQpYJiY68DeTCK5DOHg1y07tDd

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

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
-- Name: books; Type: TABLE; Schema: public; Owner: wydfaxil
--

CREATE TABLE public.books (
    id integer NOT NULL,
    name character varying NOT NULL,
    author character varying NOT NULL,
    genre character varying,
    published_date date,
    description character varying
);


ALTER TABLE public.books OWNER TO wydfaxil;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: wydfaxil
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.books_id_seq OWNER TO wydfaxil;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wydfaxil
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: wydfaxil
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_active boolean NOT NULL,
    is_admin boolean NOT NULL
);


ALTER TABLE public.users OWNER TO wydfaxil;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: wydfaxil
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO wydfaxil;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wydfaxil
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: wydfaxil
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: wydfaxil
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: wydfaxil
--

COPY public.books (id, name, author, genre, published_date, description) FROM stdin;
1	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
2	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
3	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
4	Harry Potter and the Chamber of Secrets	J.K. Rowling	Fantasy	1998-07-02	The second year at Hogwarts brings new dangers.
5	Clean Code	Robert C. Martin	Programming	2008-08-01	A handbook of agile software craftsmanship.
6	Deep Work	Cal Newport	Productivity	2016-01-05	Rules for focused success in a distracted world.
7	The Pragmatic Programmer	Andrew Hunt	Programming	1999-10-20	Journey to mastery for software developers.
8	Rich Dad Poor Dad	Robert Kiyosaki	Finance	1997-04-01	Lessons about money and investing.
9	The Psychology of Money	Morgan Housel	Finance	2020-09-08	Timeless lessons on wealth and behavior.
10	Sapiens	Yuval Noah Harari	History	2011-01-01	A brief history of humankind.
11	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
12	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
13	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
14	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
15	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
16	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
17	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
18	Harry Potter and the Chamber of Secrets	J.K. Rowling	Fantasy	1998-07-02	The second year at Hogwarts brings new dangers.
19	Harry Potter and the Prisoner of Azkaban	J.K. Rowling	Fantasy	1999-07-08	Harry discovers the truth about his past.
20	Harry Potter and the Goblet of Fire	J.K. Rowling	Fantasy	2000-07-08	The Triwizard Tournament brings new challenges.
21	Clean Code	Robert C. Martin	Programming	2008-08-01	A handbook of agile software craftsmanship.
22	Clean Code	Robert C. Martin	Programming	2008-08-01	A handbook of agile software craftsmanship.
23	Deep Work	Cal Newport	Productivity	2016-01-05	Rules for focused success in a distracted world.
24	Deep Work	Cal Newport	Productivity	2016-01-05	Rules for focused success in a distracted world.
25	The Pragmatic Programmer	Andrew Hunt	Programming	1999-10-20	Journey to mastery for software developers.
26	Rich Dad Poor Dad	Robert Kiyosaki	Finance	1997-04-01	Lessons about money and investing.
27	Rich Dad Poor Dad	Robert Kiyosaki	Finance	1997-04-01	Lessons about money and investing.
28	The Psychology of Money	Morgan Housel	Finance	2020-09-08	Timeless lessons on wealth and behavior.
29	Sapiens	Yuval Noah Harari	History	2011-01-01	A brief history of humankind.
30	Sapiens	Yuval Noah Harari	History	2011-01-01	A brief history of humankind.
31	Homo Deus	Yuval Noah Harari	History	2015-01-01	A brief history of tomorrow.
32	The Hobbit	J.R.R. Tolkien	Fantasy	1937-09-21	Bilbo Baggins embarks on an unexpected journey.
33	The Hobbit	J.R.R. Tolkien	Fantasy	1937-09-21	Bilbo Baggins embarks on an unexpected journey.
34	The Fellowship of the Ring	J.R.R. Tolkien	Fantasy	1954-07-29	The first volume in The Lord of the Rings trilogy.
35	The Two Towers	J.R.R. Tolkien	Fantasy	1954-11-11	The second volume in The Lord of the Rings trilogy.
36	The Return of the King	J.R.R. Tolkien	Fantasy	1955-10-20	The final volume in The Lord of the Rings trilogy.
37	Dune	Frank Herbert	Science Fiction	1965-08-01	A epic science fiction saga set on Arrakis.
38	Dune	Frank Herbert	Science Fiction	1965-08-01	A epic science fiction saga set on Arrakis.
39	1984	George Orwell	Fiction	1949-06-08	A dystopian novel about totalitarianism.
40	1984	George Orwell	Fiction	1949-06-08	A dystopian novel about totalitarianism.
41	To Kill a Mockingbird	Harper Lee	Fiction	1960-07-11	A story about racial injustice in the American South.
42	To Kill a Mockingbird	Harper Lee	Fiction	1960-07-11	A story about racial injustice in the American South.
43	The Great Gatsby	F. Scott Fitzgerald	Fiction	1925-04-10	A tragic story of wealth and love in the Jazz Age.
44	Pride and Prejudice	Jane Austen	Romance	1813-01-28	A classic romance novel about Elizabeth Bennet.
45	Pride and Prejudice	Jane Austen	Romance	1813-01-28	A classic romance novel about Elizabeth Bennet.
46	The Catcher in the Rye	J.D. Salinger	Fiction	1951-07-16	A story about teenage angst and alienation.
47	The Subtle Art of Not Giving a F*ck	Mark Manson	Self-help	2016-09-13	A counterintuitive approach to living a good life.
48	The Subtle Art of Not Giving a F*ck	Mark Manson	Self-help	2016-09-13	A counterintuitive approach to living a good life.
49	Can't Hurt Me	David Goggins	Self-help	2018-12-04	Master your mind and defy the odds.
50	The 7 Habits of Highly Effective People	Stephen R. Covey	Self-help	1989-08-15	Powerful lessons in personal change.
51	The 7 Habits of Highly Effective People	Stephen R. Covey	Self-help	1989-08-15	Powerful lessons in personal change.
52	Thinking, Fast and Slow	Daniel Kahneman	Psychology	2011-10-25	Insights into how our minds work.
53	Thinking, Fast and Slow	Daniel Kahneman	Psychology	2011-10-25	Insights into how our minds work.
54	The Power of Now	Eckhart Tolle	Spirituality	1997-01-01	A guide to spiritual enlightenment.
55	The 5 AM Club	Robin Sharma	Self-help	2018-12-04	Own your morning, elevate your life.
56	The 5 AM Club	Robin Sharma	Self-help	2018-12-04	Own your morning, elevate your life.
57	Grit	Angela Duckworth	Psychology	2016-05-03	The power of passion and perseverance.
58	Grit	Angela Duckworth	Psychology	2016-05-03	The power of passion and perseverance.
59	The Four Agreements	Don Miguel Ruiz	Self-help	1997-01-01	A practical guide to personal freedom.
60	The Body Keeps the Score	Bessel van der Kolk	Psychology	2014-09-25	Brain, mind, and body in the healing of trauma.
61	Educated	Tara Westover	Memoir	2018-02-20	A memoir about growing up in a survivalist family.
62	Becoming	Michelle Obama	Memoir	2018-11-13	The memoir of former First Lady Michelle Obama.
63	The Immortal Life of Henrietta Lacks	Rebecca Skloot	Science	2010-02-02	The story of cells taken without consent.
64	The Martian	Andy Weir	Science Fiction	2011-01-01	An astronaut stranded on Mars fights to survive.
65	The Martian	Andy Weir	Science Fiction	2011-01-01	An astronaut stranded on Mars fights to survive.
66	Project Hail Mary	Andy Weir	Science Fiction	2021-05-04	A lone astronaut must save humanity.
67	The Hunger Games	Suzanne Collins	Young Adult	2008-09-14	A dystopian story of survival and rebellion.
68	The Hunger Games	Suzanne Collins	Young Adult	2008-09-14	A dystopian story of survival and rebellion.
69	Catching Fire	Suzanne Collins	Young Adult	2009-09-01	The second book in The Hunger Games trilogy.
70	Mockingjay	Suzanne Collins	Young Adult	2010-08-24	The final book in The Hunger Games trilogy.
71	Twilight	Stephenie Meyer	Young Adult	2005-10-05	A vampire romance story.
72	Twilight	Stephenie Meyer	Young Adult	2005-10-05	A vampire romance story.
73	New Moon	Stephenie Meyer	Young Adult	2006-09-06	The second book in the Twilight saga.
74	Eclipse	Stephenie Meyer	Young Adult	2007-08-07	The third book in the Twilight saga.
75	Breaking Dawn	Stephenie Meyer	Young Adult	2008-08-02	The final book in the Twilight saga.
76	The Da Vinci Code	Dan Brown	Thriller	2003-03-18	A mystery thriller involving conspiracy theories.
77	The Da Vinci Code	Dan Brown	Thriller	2003-03-18	A mystery thriller involving conspiracy theories.
78	Angels & Demons	Dan Brown	Thriller	2000-05-01	Robert Langdon investigates ancient conspiracy.
79	Inferno	Dan Brown	Thriller	2013-05-14	A thriller based on Dante's Inferno.
80	The Girl with the Dragon Tattoo	Stieg Larsson	Thriller	2005-08-01	A gripping thriller about a missing person case.
81	The Silent Patient	Alex Michaelides	Thriller	2019-02-05	A psychological thriller about a woman's silence.
82	The Silent Patient	Alex Michaelides	Thriller	2019-02-05	A psychological thriller about a woman's silence.
83	Where the Crawdads Sing	Delia Owens	Fiction	2018-08-14	A story of isolation and survival in the marsh.
84	Where the Crawdads Sing	Delia Owens	Fiction	2018-08-14	A story of isolation and survival in the marsh.
85	The Night Circus	Erin Morgenstern	Fantasy	2011-09-13	A magical competition between two illusionists.
86	The Seven Husbands of Evelyn Hugo	Taylor Jenkins Reid	Fiction	2017-06-13	A Hollywood icon recounts her life and loves.
87	The Seven Husbands of Evelyn Hugo	Taylor Jenkins Reid	Fiction	2017-06-13	A Hollywood icon recounts her life and loves.
88	Daisy Jones & The Six	Taylor Jenkins Reid	Fiction	2019-03-05	The rise and fall of a fictional rock band.
89	Malibu Rising	Taylor Jenkins Reid	Fiction	2021-06-01	A family saga set in Malibu.
90	The Midnight Library	Matt Haig	Fiction	2020-08-13	A library of infinite possibilities between life and death.
91	The Midnight Library	Matt Haig	Fiction	2020-08-13	A library of infinite possibilities between life and death.
92	The Invisible Life of Addie LaRue	V.E. Schwab	Fantasy	2020-10-06	A woman who makes a deal to live forever.
93	Circe	Madeline Miller	Fantasy	2018-04-10	The story of the goddess Circe.
94	Circe	Madeline Miller	Fantasy	2018-04-10	The story of the goddess Circe.
95	The Song of Achilles	Madeline Miller	Fantasy	2011-09-20	The story of Achilles and Patroclus.
96	Verity	Colleen Hoover	Thriller	2018-12-07	A writer discovers a chilling manuscript.
97	It Ends with Us	Colleen Hoover	Romance	2016-08-02	A powerful story about love and resilience.
98	It Ends with Us	Colleen Hoover	Romance	2016-08-02	A powerful story about love and resilience.
99	Ugly Love	Colleen Hoover	Romance	2014-08-05	A story about love, loss, and healing.
100	November 9	Colleen Hoover	Romance	2015-11-10	A romance that unfolds over several years.
101	The Love Hypothesis	Ali Hazelwood	Romance	2021-09-14	A fake dating romance in academia.
102	Beach Read	Emily Henry	Romance	2020-05-19	Two writers with writer's block swap genres.
103	People We Meet on Vacation	Emily Henry	Romance	2021-05-11	Friends to lovers story over years of vacations.
104	Book Lovers	Emily Henry	Romance	2022-05-03	A romance set in the publishing world.
105	The Housemaid	Freida McFadden	Thriller	2022-08-09	A psychological thriller about a live-in maid.
106	The Housemaid	Freida McFadden	Thriller	2022-08-09	A psychological thriller about a live-in maid.
107	Never Lie	Freida McFadden	Thriller	2022-09-27	A couple finds a tape recording secrets.
108	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
109	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
110	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
111	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
112	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
113	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
114	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
115	Harry Potter and the Chamber of Secrets	J.K. Rowling	Fantasy	1998-07-02	The second year at Hogwarts brings new dangers.
116	Harry Potter and the Prisoner of Azkaban	J.K. Rowling	Fantasy	1999-07-08	Harry discovers the truth about his past.
117	Harry Potter and the Goblet of Fire	J.K. Rowling	Fantasy	2000-07-08	The Triwizard Tournament brings new challenges.
118	Clean Code	Robert C. Martin	Programming	2008-08-01	A handbook of agile software craftsmanship.
119	Clean Code	Robert C. Martin	Programming	2008-08-01	A handbook of agile software craftsmanship.
120	Deep Work	Cal Newport	Productivity	2016-01-05	Rules for focused success in a distracted world.
121	Deep Work	Cal Newport	Productivity	2016-01-05	Rules for focused success in a distracted world.
122	The Pragmatic Programmer	Andrew Hunt	Programming	1999-10-20	Journey to mastery for software developers.
123	Rich Dad Poor Dad	Robert Kiyosaki	Finance	1997-04-01	Lessons about money and investing.
124	Rich Dad Poor Dad	Robert Kiyosaki	Finance	1997-04-01	Lessons about money and investing.
125	The Psychology of Money	Morgan Housel	Finance	2020-09-08	Timeless lessons on wealth and behavior.
126	Sapiens	Yuval Noah Harari	History	2011-01-01	A brief history of humankind.
127	Sapiens	Yuval Noah Harari	History	2011-01-01	A brief history of humankind.
128	Homo Deus	Yuval Noah Harari	History	2015-01-01	A brief history of tomorrow.
129	The Hobbit	J.R.R. Tolkien	Fantasy	1937-09-21	Bilbo Baggins embarks on an unexpected journey.
130	The Hobbit	J.R.R. Tolkien	Fantasy	1937-09-21	Bilbo Baggins embarks on an unexpected journey.
131	The Fellowship of the Ring	J.R.R. Tolkien	Fantasy	1954-07-29	The first volume in The Lord of the Rings trilogy.
132	The Two Towers	J.R.R. Tolkien	Fantasy	1954-11-11	The second volume in The Lord of the Rings trilogy.
133	The Return of the King	J.R.R. Tolkien	Fantasy	1955-10-20	The final volume in The Lord of the Rings trilogy.
134	Dune	Frank Herbert	Science Fiction	1965-08-01	A epic science fiction saga set on Arrakis.
135	Dune	Frank Herbert	Science Fiction	1965-08-01	A epic science fiction saga set on Arrakis.
136	1984	George Orwell	Fiction	1949-06-08	A dystopian novel about totalitarianism.
137	1984	George Orwell	Fiction	1949-06-08	A dystopian novel about totalitarianism.
138	To Kill a Mockingbird	Harper Lee	Fiction	1960-07-11	A story about racial injustice in the American South.
139	To Kill a Mockingbird	Harper Lee	Fiction	1960-07-11	A story about racial injustice in the American South.
140	The Great Gatsby	F. Scott Fitzgerald	Fiction	1925-04-10	A tragic story of wealth and love in the Jazz Age.
141	Pride and Prejudice	Jane Austen	Romance	1813-01-28	A classic romance novel about Elizabeth Bennet.
142	Pride and Prejudice	Jane Austen	Romance	1813-01-28	A classic romance novel about Elizabeth Bennet.
143	The Catcher in the Rye	J.D. Salinger	Fiction	1951-07-16	A story about teenage angst and alienation.
144	The Subtle Art of Not Giving a F*ck	Mark Manson	Self-help	2016-09-13	A counterintuitive approach to living a good life.
145	The Subtle Art of Not Giving a F*ck	Mark Manson	Self-help	2016-09-13	A counterintuitive approach to living a good life.
146	Can't Hurt Me	David Goggins	Self-help	2018-12-04	Master your mind and defy the odds.
147	The 7 Habits of Highly Effective People	Stephen R. Covey	Self-help	1989-08-15	Powerful lessons in personal change.
148	The 7 Habits of Highly Effective People	Stephen R. Covey	Self-help	1989-08-15	Powerful lessons in personal change.
149	Thinking, Fast and Slow	Daniel Kahneman	Psychology	2011-10-25	Insights into how our minds work.
150	Thinking, Fast and Slow	Daniel Kahneman	Psychology	2011-10-25	Insights into how our minds work.
151	The Power of Now	Eckhart Tolle	Spirituality	1997-01-01	A guide to spiritual enlightenment.
152	The 5 AM Club	Robin Sharma	Self-help	2018-12-04	Own your morning, elevate your life.
153	The 5 AM Club	Robin Sharma	Self-help	2018-12-04	Own your morning, elevate your life.
154	Grit	Angela Duckworth	Psychology	2016-05-03	The power of passion and perseverance.
155	Grit	Angela Duckworth	Psychology	2016-05-03	The power of passion and perseverance.
156	The Four Agreements	Don Miguel Ruiz	Self-help	1997-01-01	A practical guide to personal freedom.
157	The Four Agreements	Don Miguel Ruiz	Self-help	1997-01-01	A practical guide to personal freedom.
158	The Body Keeps the Score	Bessel van der Kolk	Psychology	2014-09-25	Brain, mind, and body in the healing of trauma.
159	The Body Keeps the Score	Bessel van der Kolk	Psychology	2014-09-25	Brain, mind, and body in the healing of trauma.
160	Educated	Tara Westover	Memoir	2018-02-20	A memoir about growing up in a survivalist family.
161	Becoming	Michelle Obama	Memoir	2018-11-13	The memoir of former First Lady Michelle Obama.
162	Becoming	Michelle Obama	Memoir	2018-11-13	The memoir of former First Lady Michelle Obama.
163	The Immortal Life of Henrietta Lacks	Rebecca Skloot	Science	2010-02-02	The story of cells taken without consent.
164	The Immortal Life of Henrietta Lacks	Rebecca Skloot	Science	2010-02-02	The story of cells taken without consent.
165	The Martian	Andy Weir	Science Fiction	2011-01-01	An astronaut stranded on Mars fights to survive.
166	The Martian	Andy Weir	Science Fiction	2011-01-01	An astronaut stranded on Mars fights to survive.
167	Project Hail Mary	Andy Weir	Science Fiction	2021-05-04	A lone astronaut must save humanity.
168	The Hunger Games	Suzanne Collins	Young Adult	2008-09-14	A dystopian story of survival and rebellion.
169	The Hunger Games	Suzanne Collins	Young Adult	2008-09-14	A dystopian story of survival and rebellion.
170	Catching Fire	Suzanne Collins	Young Adult	2009-09-01	The second book in The Hunger Games trilogy.
171	Mockingjay	Suzanne Collins	Young Adult	2010-08-24	The final book in The Hunger Games trilogy.
172	Twilight	Stephenie Meyer	Young Adult	2005-10-05	A vampire romance story.
173	Twilight	Stephenie Meyer	Young Adult	2005-10-05	A vampire romance story.
174	New Moon	Stephenie Meyer	Young Adult	2006-09-06	The second book in the Twilight saga.
175	Eclipse	Stephenie Meyer	Young Adult	2007-08-07	The third book in the Twilight saga.
176	Breaking Dawn	Stephenie Meyer	Young Adult	2008-08-02	The final book in the Twilight saga.
177	The Da Vinci Code	Dan Brown	Thriller	2003-03-18	A mystery thriller involving conspiracy theories.
178	The Da Vinci Code	Dan Brown	Thriller	2003-03-18	A mystery thriller involving conspiracy theories.
179	Angels & Demons	Dan Brown	Thriller	2000-05-01	Robert Langdon investigates ancient conspiracy.
180	Inferno	Dan Brown	Thriller	2013-05-14	A thriller based on Dante's Inferno.
181	The Girl with the Dragon Tattoo	Stieg Larsson	Thriller	2005-08-01	A gripping thriller about a missing person case.
182	The Girl with the Dragon Tattoo	Stieg Larsson	Thriller	2005-08-01	A gripping thriller about a missing person case.
183	The Silent Patient	Alex Michaelides	Thriller	2019-02-05	A psychological thriller about a woman's silence.
184	The Silent Patient	Alex Michaelides	Thriller	2019-02-05	A psychological thriller about a woman's silence.
185	Where the Crawdads Sing	Delia Owens	Fiction	2018-08-14	A story of isolation and survival in the marsh.
186	Where the Crawdads Sing	Delia Owens	Fiction	2018-08-14	A story of isolation and survival in the marsh.
187	The Night Circus	Erin Morgenstern	Fantasy	2011-09-13	A magical competition between two illusionists.
188	The Night Circus	Erin Morgenstern	Fantasy	2011-09-13	A magical competition between two illusionists.
189	The Seven Husbands of Evelyn Hugo	Taylor Jenkins Reid	Fiction	2017-06-13	A Hollywood icon recounts her life and loves.
190	The Seven Husbands of Evelyn Hugo	Taylor Jenkins Reid	Fiction	2017-06-13	A Hollywood icon recounts her life and loves.
191	Daisy Jones & The Six	Taylor Jenkins Reid	Fiction	2019-03-05	The rise and fall of a fictional rock band.
192	Malibu Rising	Taylor Jenkins Reid	Fiction	2021-06-01	A family saga set in Malibu.
193	The Midnight Library	Matt Haig	Fiction	2020-08-13	A library of infinite possibilities between life and death.
194	The Midnight Library	Matt Haig	Fiction	2020-08-13	A library of infinite possibilities between life and death.
195	The Invisible Life of Addie LaRue	V.E. Schwab	Fantasy	2020-10-06	A woman who makes a deal to live forever.
196	The Invisible Life of Addie LaRue	V.E. Schwab	Fantasy	2020-10-06	A woman who makes a deal to live forever.
197	Circe	Madeline Miller	Fantasy	2018-04-10	The story of the goddess Circe.
198	Circe	Madeline Miller	Fantasy	2018-04-10	The story of the goddess Circe.
199	The Song of Achilles	Madeline Miller	Fantasy	2011-09-20	The story of Achilles and Patroclus.
200	The Song of Achilles	Madeline Miller	Fantasy	2011-09-20	The story of Achilles and Patroclus.
201	The Silent Patient	Alex Michaelides	Thriller	2019-02-05	A psychological thriller about a woman's silence.
202	The Maidens	Alex Michaelides	Thriller	2021-06-15	A murder mystery set at Cambridge University.
203	The Guest List	Lucy Foley	Thriller	2020-06-02	A wedding turns deadly on a remote island.
204	The Guest List	Lucy Foley	Thriller	2020-06-02	A wedding turns deadly on a remote island.
205	The Hunting Party	Lucy Foley	Thriller	2019-02-05	A New Year's Eve celebration turns deadly.
206	The Paris Apartment	Lucy Foley	Thriller	2022-02-22	A mystery set in a Paris apartment building.
207	Verity	Colleen Hoover	Thriller	2018-12-07	A writer discovers a chilling manuscript.
208	Verity	Colleen Hoover	Thriller	2018-12-07	A writer discovers a chilling manuscript.
209	It Ends with Us	Colleen Hoover	Romance	2016-08-02	A powerful story about love and resilience.
210	It Ends with Us	Colleen Hoover	Romance	2016-08-02	A powerful story about love and resilience.
211	It Starts with Us	Colleen Hoover	Romance	2022-10-18	The sequel to It Ends with Us.
212	Ugly Love	Colleen Hoover	Romance	2014-08-05	A story about love, loss, and healing.
213	November 9	Colleen Hoover	Romance	2015-11-10	A romance that unfolds over several years.
214	Reminders of Him	Colleen Hoover	Romance	2022-01-18	A story of redemption and second chances.
215	The Love Hypothesis	Ali Hazelwood	Romance	2021-09-14	A fake dating romance in academia.
216	The Love Hypothesis	Ali Hazelwood	Romance	2021-09-14	A fake dating romance in academia.
217	Love on the Brain	Ali Hazelwood	Romance	2022-08-23	A STEM romance about rivals to lovers.
218	Beach Read	Emily Henry	Romance	2020-05-19	Two writers with writer's block swap genres.
219	Beach Read	Emily Henry	Romance	2020-05-19	Two writers with writer's block swap genres.
220	People We Meet on Vacation	Emily Henry	Romance	2021-05-11	Friends to lovers story over years of vacations.
221	Book Lovers	Emily Henry	Romance	2022-05-03	A romance set in the publishing world.
222	Happy Place	Emily Henry	Romance	2023-04-25	A couple pretends to still be together.
223	The Housemaid	Freida McFadden	Thriller	2022-08-09	A psychological thriller about a live-in maid.
224	The Housemaid	Freida McFadden	Thriller	2022-08-09	A psychological thriller about a live-in maid.
225	The Housemaid's Secret	Freida McFadden	Thriller	2023-07-11	The sequel to The Housemaid.
226	The Coworker	Freida McFadden	Thriller	2023-08-29	A workplace thriller.
227	Never Lie	Freida McFadden	Thriller	2022-09-27	A couple finds a tape recording secrets.
228	The Inmate	Freida McFadden	Thriller	2022-01-01	A nurse works at a prison with her ex-boyfriend.
229	The Locked Door	Freida McFadden	Thriller	2021-01-01	A surgeon with a dark past.
230	Ward D	Freida McFadden	Thriller	2023-01-01	A medical student's overnight shift in a psych ward.
231	The Perfect Son	Freida McFadden	Thriller	2022-01-01	A mother suspects her son of murder.
232	One by One	Freida McFadden	Thriller	2022-01-01	A group of friends are killed one by one.
233	The Teacher	Freida McFadden	Thriller	2023-01-01	A teacher with a dangerous secret.
234	The Boyfriend	Freida McFadden	Thriller	2023-01-01	A woman's new boyfriend might be dangerous.
235	The Surrogate Mother	Freida McFadden	Thriller	2021-01-01	A couple's surrogate has dark intentions.
236	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
237	Atomic Habits	James Clear	Self-help	2018-10-16	A guide to building good habits and breaking bad ones.
238	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
239	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
240	The Alchemist	Paulo Coelho	Fiction	1988-04-15	A philosophical story about following your dreams.
241	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
242	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
243	Harry Potter and the Sorcerer's Stone	J.K. Rowling	Fantasy	1997-06-26	A young wizard begins his magical journey.
244	Harry Potter and the Chamber of Secrets	J.K. Rowling	Fantasy	1998-07-02	The second year at Hogwarts brings new dangers.
245	PEER-E-KAMIL	IDK	SUFI	2026-03-26	KABHI PARHI NAHI BRO
246	Test Book	Fazil Naeem	Education	2026-03-11	Testing wrapper
247	Test Book	Fazil Naeem	Education	2026-03-11	Testing wrapper
248	DIL_E_KHAWABZAD	Arslan Abbas	Poetry	2026-04-02	Udaas, kyu, ho
249	string	string	string	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: wydfaxil
--

COPY public.users (id, username, email, hashed_password, is_active, is_admin) FROM stdin;
1	wydfaxil	a.faazil07@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$QbVHEuXc6Fmxto642OQrwu$e6RdbLlR4wqL9yJQIUovn52eRP0mFy6	t	t
2	Ahmed Fazil	SP22-BSE-108@cuilahore.edu.pk	$bcrypt-sha256$v=2,t=2b,r=12$iWKQgv8yzMQb9A8W5Wtvye$bEqc9gyKkolV.sSjYEfuOTvkmvu/p9K	t	f
\.


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wydfaxil
--

SELECT pg_catalog.setval('public.books_id_seq', 249, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wydfaxil
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: wydfaxil
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: wydfaxil
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_books_author; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE INDEX ix_books_author ON public.books USING btree (author);


--
-- Name: ix_books_genre; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE INDEX ix_books_genre ON public.books USING btree (genre);


--
-- Name: ix_books_id; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE INDEX ix_books_id ON public.books USING btree (id);


--
-- Name: ix_books_name; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE INDEX ix_books_name ON public.books USING btree (name);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: wydfaxil
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO wydfaxil;


--
-- PostgreSQL database dump complete
--

\unrestrict xTGOjMEbXzoDQJbnaQvpTr1CGPhs2uGz6g7eTOQpYJiY68DeTCK5DOHg1y07tDd

