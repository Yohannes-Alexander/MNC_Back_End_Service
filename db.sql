CREATE TABLE public.users (
	user_id varchar NOT NULL,
	first_name varchar NULL,
	last_name varchar NULL,
	phone_number varchar NULL,
	address varchar NULL,
	pin varchar NULL,
	refresh_token varchar NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamp NULL,
	balance int8 NULL DEFAULT '0'::bigint,
	CONSTRAINT user_pkey PRIMARY KEY (user_id)
);


CREATE TABLE public.payments (
	payment_id varchar NOT NULL,
	amount int8 NULL,
	remarks varchar NULL,
	balance_before int8 NULL,
	balance_after int8 NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamp NULL,
	user_id varchar NULL,
	status varchar NULL,
	transaction_type varchar NULL,
	CONSTRAINT payments_pkey PRIMARY KEY (payment_id),
	CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id)
);




CREATE TABLE public.top_up (
	top_up_id varchar NOT NULL,
	amount_top_up int8 NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamp NULL,
	user_id varchar NULL,
	balance_before int8 NULL,
	balance_after int8 NULL,
	status varchar NULL,
	transaction_type varchar NULL,
	CONSTRAINT top_up_pkey PRIMARY KEY (top_up_id),
	CONSTRAINT top_up_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL
);


CREATE TABLE public.transfers (
	transfer_id varchar NOT NULL,
	amount int8 NULL,
	remarks varchar NULL,
	balance_before int8 NULL,
	balance_after int8 NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamp NULL,
	user_id varchar NULL,
	target_user_id varchar NULL,
	status varchar NULL,
	transaction_type varchar NULL,
	CONSTRAINT transfers_pkey PRIMARY KEY (transfer_id),
	CONSTRAINT transfers_target_user_id_fkey FOREIGN KEY (target_user_id) REFERENCES public.users(user_id),
	CONSTRAINT transfers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL
);