-- Project Group 102

-- Team Members Names:
-- Luis Sosa Lora 
-- Paola Cernada

-- Project Title:
-- Board Game Rentals

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_cernadap`
--

-- --------------------------------------------------------

--
-- Table structure for table `board_games`
--

CREATE TABLE `board_games` (
  `bg_id` int(11) NOT NULL,
  `bg_name` varchar(75) NOT NULL,
  `daily_rental_rate` decimal(5,2) NOT NULL,
  `number_of_copies_in_stock` int(10) UNSIGNED NOT NULL,
  `available_to_rent` int(10) UNSIGNED NOT NULL,
  `quantity_checked_out` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `board_games`
--

INSERT INTO `board_games` (`bg_id`, `bg_name`, `daily_rental_rate`, `number_of_copies_in_stock`, `available_to_rent`, `quantity_checked_out`) VALUES
(1, 'Azul', 5.00, 25, 24, 1),
(2, 'Ticket to Ride', 10.00, 30, 28, 2),
(3, 'Splendor', 12.00, 10, 9, 1),
(4, 'Wingspan', 15.00, 22, 21, 1);

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `customer_name` varchar(75) NOT NULL,
  `email` varchar(320) NOT NULL,
  `total_quantity_of_bgs_checked_out` int(10) UNSIGNED NOT NULL,
  `total_amount_spent` decimal(5,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `customer_name`, `email`, `total_quantity_of_bgs_checked_out`, `total_amount_spent`) VALUES
(1, 'John Blue', 'jb@gmail.com', 1, 48.00),
(2, 'Laura Kent', 'laurak@email.com', 2, 65.00),
(3, 'Paul Smith', 'psmith@live.com', 1, 45.00),
(4, 'Clark Thomas', 'cthomas@yahoo.com', 1, 70.00);

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `employee_id` int(11) NOT NULL,
  `employee_full_name` varchar(75) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `employee_full_name`) VALUES
(1, 'Jacob Sanders'),
(2, 'Lola Perez'),
(3, 'Matt Lee'),
(4, 'Kim Miller');

-- --------------------------------------------------------

--
-- Table structure for table `invoices`
--

CREATE TABLE `invoices` (
  `invoice_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `date_checked_out` date NOT NULL,
  `total_due` decimal(5,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `invoices`
--

INSERT INTO `invoices` (`invoice_id`, `customer_id`, `employee_id`, `date_checked_out`, `total_due`) VALUES
(1, 4, NULL, '2023-05-16', 35.00),
(2, 2, 1, '2023-05-17', 15.00),
(3, 1, 3, '2023-05-15', 48.00),
(4, 3, NULL, '2023-05-16', 45.00),
(5, 2, NULL, '2023-05-18', 50.00);

-- --------------------------------------------------------

--
-- Table structure for table `invoice_details`
--

CREATE TABLE `invoice_details` (
  `invoice_details_id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `bg_id` int(11) NOT NULL,
  `length_of_rental` int(10) UNSIGNED NOT NULL,
  `daily_rental_rate` decimal(5,2) UNSIGNED NOT NULL,
  `line_total` decimal(5,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `invoice_details`
--

INSERT INTO `invoice_details` (`invoice_details_id`, `invoice_id`, `bg_id`, `length_of_rental`, `daily_rental_rate`, `line_total`) VALUES
(27, 1, 2, 7, 10.00, 70.00),
(28, 2, 1, 3, 5.00, 15.00),
(29, 3, 3, 4, 12.00, 48.00),
(30, 4, 4, 3, 15.00, 45.00),
(31, 5, 2, 5, 10.00, 50.00);

--
-- Triggers `invoice_details`
--
DELIMITER $$
CREATE TRIGGER `update_total_due_and_quantity` AFTER INSERT ON `invoice_details` FOR EACH ROW BEGIN
    -- Calculate the new total_due based on the inserted line_total
    DECLARE new_total_due DECIMAL(5,2);
    SELECT SUM(line_total) INTO new_total_due
    FROM invoice_details
    WHERE invoice_id = NEW.invoice_id;

    -- Update the total_due in the invoices table
    UPDATE invoices
    SET total_due = new_total_due
    WHERE invoice_id = NEW.invoice_id;

    -- Update the total_quantity_of_bgs_checked_out in the customers table
    UPDATE customers
    SET total_quantity_of_bgs_checked_out = (
        SELECT SUM(length_of_rental)
        FROM invoice_details
        WHERE invoice_id = NEW.invoice_id
    )
    WHERE customer_id = (
        SELECT customer_id
        FROM invoices
        WHERE invoice_id = NEW.invoice_id
    );

    -- Increment the quantity_checked_out in the board_games table
    UPDATE board_games
    SET quantity_checked_out = quantity_checked_out + 1
    WHERE bg_id = NEW.bg_id;

    -- Calculate the available_to_rent in the board_games table
    UPDATE board_games
    SET available_to_rent = number_of_copies_in_stock - quantity_checked_out;

    -- Update the total_amount_spent in the customers table
    UPDATE customers
    SET total_amount_spent = (
        SELECT SUM(line_total)
        FROM invoice_details
        JOIN invoices ON invoice_details.invoice_id = invoices.invoice_id
        WHERE invoices.customer_id = (
            SELECT customer_id
            FROM invoices
            WHERE invoice_id = NEW.invoice_id
        )
    )
    WHERE customer_id = (
        SELECT customer_id
        FROM invoices
        WHERE invoice_id = NEW.invoice_id
    );
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `board_games`
--
ALTER TABLE `board_games`
  ADD PRIMARY KEY (`bg_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`invoice_id`),
  ADD KEY `fk_customers_id` (`customer_id`),
  ADD KEY `fk_employee_id` (`employee_id`);

--
-- Indexes for table `invoice_details`
--
ALTER TABLE `invoice_details`
  ADD PRIMARY KEY (`invoice_details_id`),
  ADD KEY `fk_bg_id` (`bg_id`),
  ADD KEY `fk_invoice_id` (`invoice_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `board_games`
--
ALTER TABLE `board_games`
  MODIFY `bg_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `invoices`
--
ALTER TABLE `invoices`
  MODIFY `invoice_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `invoice_details`
--
ALTER TABLE `invoice_details`
  MODIFY `invoice_details_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `fk_customers_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `invoice_details`
--
ALTER TABLE `invoice_details`
  ADD CONSTRAINT `fk_bg_id` FOREIGN KEY (`bg_id`) REFERENCES `board_games` (`bg_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `invoices` (`invoice_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
