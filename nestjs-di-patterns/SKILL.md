---
name: nestjs-di-patterns
description: Guia para uso de interfaces vs classes abstratas no NestJS DI. Use quando criar repositórios, services ou qualquer abstração que será injetada via DI.
---

# NestJS DI: Interfaces vs Abstract Classes

## Regra Principal

| Cenário | Use | Motivo |
|---------|-----|--------|
| Token de injeção (DI) | `abstract class` | TypeScript apaga interfaces em runtime |
| Contratos segregados (ISP) | `interface` | Não precisa de token, apenas tipagem |

## Padrão: Interface Segregation + Abstract Class

```typescript
// Interfaces segregadas (ISP) - contratos granulares
export interface FindByIdRepository {
  findById(id: string): Promise<Either<string, Entity>>
}

export interface SaveRepository {
  save(entity: Entity): Promise<Either<string, Entity>>
}

// Abstract class para DI - implementa as interfaces
export abstract class EntityRepository
  implements FindByIdRepository, SaveRepository
{
  abstract findById(id: string): Promise<Either<string, Entity>>
  abstract save(entity: Entity): Promise<Either<string, Entity>>
}
```

## No Module

```typescript
// A abstract class serve como token
providers: [
  { provide: EntityRepository, useClass: EntityOrmRepository }
]
```

## No Handler/Service

```typescript
// Injeta usando a abstract class como tipo
constructor(private readonly repository: EntityRepository) {}
```

## Por que não usar interface direto?

```typescript
// ❌ Não funciona - interface não existe em runtime
{ provide: IEntityRepository, useClass: EntityOrmRepository }
//         ^^^^^^^^^^^^^^^^^ undefined em runtime

// ✅ Funciona - abstract class existe em runtime
{ provide: EntityRepository, useClass: EntityOrmRepository }
```

## Resumo

1. **Interfaces** → contratos segregados (ISP), tipagem estática
2. **Abstract class** → token de DI, implementa as interfaces
3. **Concrete class** → implementa a abstract class
