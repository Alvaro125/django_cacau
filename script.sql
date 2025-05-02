-- Companies table
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    tax_id VARCHAR(18) UNIQUE,
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    position VARCHAR(50),
    is_admin BOOLEAN DEFAULT FALSE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Work schedule table
CREATE TABLE work_schedules (
    schedule_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    weekday INT NOT NULL, -- 0 = Sunday, 1 = Monday, etc.
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    CONSTRAINT unique_employee_schedule UNIQUE (employee_id, weekday, start_time)
);

-- Services table
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    duration INT NOT NULL, -- in minutes
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Services assigned to employees table
CREATE TABLE employee_services (
    employee_service_id SERIAL PRIMARY KEY,
    service_id INT NOT NULL,
    employee_id INT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    CONSTRAINT unique_service_employee UNIQUE (service_id, employee_id)
);

-- Customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers associated with companies table
CREATE TABLE company_customers (
    customer_id INT NOT NULL,
    company_id INT NOT NULL,
    association_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, company_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Appointments table
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    employee_service_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, completed, canceled, rejected
    notes TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_service_id) REFERENCES employee_services(employee_service_id) ON DELETE CASCADE
);

-- Service receipts table
CREATE TABLE service_receipts (
    receipt_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL,
    receipt_code VARCHAR(50) UNIQUE NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, canceled, rejected
    employee_notes TEXT,
    customer_notes TEXT,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE
);

-- Company minisite configuration table
CREATE TABLE minisite_config (
    company_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    logo_url VARCHAR(255),
    primary_color VARCHAR(7) DEFAULT '#000000',
    secondary_color VARCHAR(7) DEFAULT '#FFFFFF',
    social_facebook VARCHAR(255),
    social_instagram VARCHAR(255),
    social_whatsapp VARCHAR(20),
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Minisite access logs table
CREATE TABLE minisite_access_logs (
    access_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    access_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Indexes to improve performance
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_services_company ON services(company_id);
CREATE INDEX idx_employees_company ON employees(company_id);
CREATE INDEX idx_receipts_status ON service_receipts(status);

-- Triggers for automatic updates
-- Trigger to automatically set company owner as admin employee
CREATE OR REPLACE FUNCTION create_admin_employee()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employees (company_id, name, email, password, position, is_admin)
    VALUES (NEW.company_id, NEW.name, NEW.email, NEW.password, 'Owner', TRUE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_create_admin_employee
AFTER INSERT ON companies
FOR EACH ROW
EXECUTE FUNCTION create_admin_employee();

-- Trigger to automatically create a minisite configuration record for each new company
CREATE OR REPLACE FUNCTION create_minisite_config()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO minisite_config (company_id, title, description)
    VALUES (NEW.company_id, NEW.name, 'Minisite for ' || NEW.name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_create_minisite_config
AFTER INSERT ON companies
FOR EACH ROW
EXECUTE FUNCTION create_minisite_config();

-- Trigger to automatically create a receipt when an appointment is created
CREATE OR REPLACE FUNCTION create_receipt()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO service_receipts (appointment_id, receipt_code)
    VALUES (NEW.appointment_id, 'RCPT-' || NEW.appointment_id || '-' || to_char(NOW(), 'YYYYMMDDHH24MISS'));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_create_receipt
AFTER INSERT ON appointments
FOR EACH ROW
EXECUTE FUNCTION create_receipt();

-- Trigger to update receipt status when appointment status is changed
CREATE OR REPLACE FUNCTION update_receipt_status()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE service_receipts
    SET status = NEW.status
    WHERE appointment_id = NEW.appointment_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_update_receipt_status
AFTER UPDATE OF status ON appointments
FOR EACH ROW
EXECUTE FUNCTION update_receipt_status();