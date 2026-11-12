# MediWeave – Database Architecture

## 1. Database Technology

Primary database: PostgreSQL.

ORM: SQLAlchemy.

Database migration tool: Alembic.

## 2. Database Design Approach

MediWeave will initially use a shared PostgreSQL database with a shared schema and logical tenant separation.

The database will follow relational database design principles and normalization.

## 3. Initial Entities

1. Users
2. Pharmacies
3. Pharmacy Memberships
4. Ingredients
5. Formulations
6. Formulation Ingredients
7. Medicine Products
8. Inventory
9. Inventory Events
10. Reservations

## 4. Important Relationships

- A user can belong to multiple pharmacies.
- A pharmacy can have multiple users.
- A pharmacy can stock multiple medicine products.
- A medicine product can be stocked by multiple pharmacies.
- A formulation can contain multiple active ingredients.
- An active ingredient can belong to multiple formulations.
- An inventory record can have multiple associated inventory events.
- An inventory record can be associated with multiple reservations over time.

## 5. Medicine Data Model

Medicine identity will be separated into:

- Active ingredient.
- Formulation.
- Marketed medicine product.
- Product packaging.

This separation supports accurate formulation matching and prevents confusion between different strengths, dosage forms and brands.

## 6. Inventory Management

Inventory records will be pharmacy-specific.

Inventory information will include:

- Physical quantity.
- Reserved quantity.
- Available quantity.
- Last synchronization timestamp.
- Inventory source.
- Version information.

## 7. Inventory Event Management

Inventory changes will be recorded as events to support:

- Auditability.
- Synchronization.
- Duplicate event detection.
- Conflict resolution.
- Reconciliation.

## 8. Reservation Management

Reservations will use database transactions and concurrency controls to prevent overselling.

## 9. Security

Pharmacy data will be isolated using tenant-aware authorization and database access controls.

Users will access pharmacy operations according to their assigned roles and permissions.