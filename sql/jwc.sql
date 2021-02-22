create table t_jwc_news
(
    id bigserial,
    title varchar(255),
    url varchar(255),
    date varchar(255),

    primary key (id),
    unique (url)
);