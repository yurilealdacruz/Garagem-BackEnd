/*
  Warnings:

  - You are about to drop the column `criadoEm` on the `Evento` table. All the data in the column will be lost.
  - Added the required column `garagemId` to the `Evento` table without a default value. This is not possible if the table is not empty.

*/
-- CreateTable
CREATE TABLE "Garagem" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nome" TEXT NOT NULL
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Evento" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "tipo" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "garagemId" INTEGER NOT NULL,
    CONSTRAINT "Evento_garagemId_fkey" FOREIGN KEY ("garagemId") REFERENCES "Garagem" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Evento" ("id", "tipo") SELECT "id", "tipo" FROM "Evento";
DROP TABLE "Evento";
ALTER TABLE "new_Evento" RENAME TO "Evento";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;

-- CreateIndex
CREATE UNIQUE INDEX "Garagem_nome_key" ON "Garagem"("nome");
