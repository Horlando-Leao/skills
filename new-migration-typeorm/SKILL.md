---
name: new-migration-typeorm
description: Create TypeORM migrations using native CLI commands. Use when creating database migrations, schema changes, adding/removing columns, or modifying table structure.
---

# TypeORM Migrations

## Quick Reference

| Command  | Script                                        | Use Case                          |
| -------- | --------------------------------------------- | --------------------------------- |
| Generate | `npm run migration:generate <Name>` | Auto-generate from entity changes |
| Create   | `npm run migration:create <Name>`   | Create blank migration            |
| Run      | `npm run migration:run`             | Execute pending migrations        |
| Revert   | `npm run migration:revert`          | Rollback last migration           |

## Choosing Between Generate vs Create

**Generate** (`migration:generate`): Use when you modified entities and want
TypeORM to auto-detect changes.

**Create** (`migration:create`): Use for:

- Custom SQL (indexes, constraints, seeds)
- Changes not reflected in entities
- Complex data transformations

## Migration Naming Convention

Use PascalCase describing the change:

```
AddColumnToTable
CreateTableName
RemoveColumnFromTable
AddIndexOnTableColumn
SeedInitialData
```

## Creating a Migration

### Option 1: Generate from Entity Changes

1. Modify your entity file
2. Run:

```bash
npm run migration:generate AddColumnToTable
```

### Option 2: Create Blank Migration

```bash
npm run migration:create AddColumnToTable
```

## Migration File Structure

```typescript
import { MigrationInterface, QueryRunner } from "typeorm";

export class AddColumnToTable1776000000000 implements MigrationInterface {
  name = "AddColumnToTable1776000000000";

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE "table_name" 
      ADD COLUMN "column_name" character varying
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE "table_name" 
      DROP COLUMN "column_name"
    `);
  }
}
```

## Database Conventions

Follow the [data-base skill](../data-base/SKILL.md):

- **Tables**: plural, snake_case (`users`, `documents`)
- **Columns**: snake_case (`created_at`, `user_id`)
- **Primary keys**: UUIDv7
- **Audit fields**: `id`, `created_at`, `updated_at`, `deleted_at` (nullable)
- **Timestamps**: ISO-8601 UTC with `TIMESTAMP WITH TIME ZONE`

## Workflow Checklist

```
Migration Checklist:
- [ ] Choose generate vs create based on use case
- [ ] Use descriptive PascalCase name
- [ ] Implement both up() and down() methods
- [ ] Follow snake_case naming for tables/columns
- [ ] Include audit fields for new tables
- [ ] Test migration locally before committing
```

## Running Migrations

```bash
# Execute all pending migrations
npm run migration:run

# Revert last migration (repeat for multiple)
npm run migration:revert
```

## Troubleshooting

**Migration not detected**: Ensure `ormconfig.ts` includes the migrations path
and entities are registered.

**Connection refused**: Check `.env` database credentials (`DATABASE_HOST`,
`DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`).

**down() fails**: Always test revert before pushing. The `down()` must be the
exact inverse of `up()`.
