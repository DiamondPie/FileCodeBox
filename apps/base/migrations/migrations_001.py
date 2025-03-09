from tortoise import connections


async def create_file_codes_table():
    conn = connections.get("default")
    await conn.execute_script(
        """
        CREATE TABLE IF NOT EXISTS filecodes
        (
            id             INTEGER                                not null
                primary key AUTO_INCREMENT,
            code           VARCHAR(255)                           not null,
            prefix         VARCHAR(255) default ''                not null,
            suffix         VARCHAR(255) default ''                not null,
            uuid_file_name VARCHAR(255),
            file_path      VARCHAR(255),
            size           INT          default 0                 not null,
            text           TEXT,
            expired_at     TIMESTAMP,
            expired_count  INT          default 0                 not null,
            used_count     INT          default 0                 not null,
            created_at     TIMESTAMP    default CURRENT_TIMESTAMP not null,
            UNIQUE (code)
        );
    """
    )
    # 检查索引是否存在，如果不存在则创建
    index_exists = await conn.execute_query(
        "SELECT 1 FROM information_schema.statistics WHERE table_name = 'filecodes' AND index_name = 'idx_filecodes_code_1c7ee7';"
    )
    if not index_exists[1]:
        await conn.execute_script(
            "CREATE INDEX idx_filecodes_code_1c7ee7 ON filecodes (code);"
        )


async def create_key_value_table():
    conn = connections.get("default")
    await conn.execute_script(
        """
        CREATE TABLE IF NOT EXISTS keyvalue
        (
            id         INTEGER                             not null
                primary key AUTO_INCREMENT,
            `key`        VARCHAR(255)                        not null,
            `value`      JSON,
            created_at TIMESTAMP default CURRENT_TIMESTAMP not null,
            UNIQUE (`key`)
        );
    """
    )
    # 检查索引是否存在，如果不存在则创建
    index_exists = await conn.execute_query(
        "SELECT 1 FROM information_schema.statistics WHERE table_name = 'keyvalue' AND index_name = 'idx_keyvalue_key_eab890';"
    )
    if not index_exists[1]:
        await conn.execute_script(
            "CREATE INDEX idx_keyvalue_key_eab890 ON keyvalue (`key`);"
        )


async def migrate():
    await create_file_codes_table()
    await create_key_value_table()
