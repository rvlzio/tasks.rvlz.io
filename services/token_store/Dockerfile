FROM redis:6.2.6-alpine

ARG TOKEN_STORE_PASSWORD
ENV TOKEN_STORE_PASSWORD ${TOKEN_STORE_PASSWORD}

CMD redis-server --requirepass ${TOKEN_STORE_PASSWORD}
