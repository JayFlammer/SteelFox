CREATE TABLE stahlpreise (
    id SERIAL PRIMARY KEY,       -- Automatische ID als Primärschlüssel
    produktcode VARCHAR(50) NOT NULL,  -- Produktcode, z. B. Stahltyp oder Referenz
    name VARCHAR(255) NOT NULL,  -- Name des Produkts (z. B. "Baustahl")
    datum DATE NOT NULL,         -- Datum, an dem der Preis gilt
    preis DECIMAL(10, 2) NOT NULL  -- Preis in der gewünschten Währung (z. B. EUR/Tonne)
);
