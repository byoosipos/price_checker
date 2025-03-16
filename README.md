# Price Checker

A modern, user-friendly barcode scanning application built for Metro Supermarket to allow customers to quickly check prices of items in-store.

![Price Checker Screenshot](price_checker/www/logometro.png)

## Features

- **Fast Barcode Scanning**: Supports both manual entry and barcode scanner devices
- **Responsive Design**: Works on kiosks, tablets, and mobile devices
- **Real-time Price Lookup**: Instantly retrieves current pricing information
- **Item Details Display**: Shows product name, code, group, image, and price
- **Customer Feedback System**: Built-in rating system for customer satisfaction tracking
- **Automatic Focus Management**: Cursor always stays in the scan area for seamless scanning
- **Caching System**: LRU (Least Recently Used) caching for frequently scanned items
- **Fullscreen Mode**: Optimized for kiosk displays
- **Screen Wake Lock**: Prevents device from sleeping during operation
- **Attractive UI**: Modern interface with animations and visual feedback

## Installation

### Prerequisites

- Frappe Framework
- ERPNext (recommended)
- Node.js and npm

### Setup

1. Navigate to your bench directory:
   ```
   cd frappe-bench
   ```

2. Get the Price Checker app from GitHub:
   ```
   bench get-app price_checker https://github.com/yourusername/price_checker
   ```

3. Install the app on your site:
   ```
   bench --site your-site.com install-app price_checker
   ```

4. Run migrations:
   ```
   bench --site your-site.com migrate
   ```

5. Build assets:
   ```
   bench build
   ```

6. Restart the server:
   ```
   bench restart
   ```

## Usage

1. Access the Price Checker at: `https://your-site.com/price_check`
2. Scan a barcode using a USB barcode scanner or manually enter the barcode number
3. View the item details and price information
4. Optionally provide feedback using the rating system

## Configuration

The Price Checker can be configured through the Frappe interface:

- **Selling Settings**: Controls the price list used for displaying prices
- **Item Master**: Manages item information including images and barcodes
- **Item Price**: Sets the prices that will be displayed

## Development

### Structure

- `price_checker/www/price_check.html` - Main application interface
- `price_checker/api.py` - Backend API for barcode lookups
- `price_checker/hooks.py` - Frappe hooks configuration

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/price_checker
   ```

2. Link to your bench:
   ```
   bench --site your-site.com add-to-hosts
   cd frappe-bench
   bench setup symlinks
   ```

3. Start development server:
   ```
   bench start
   ```

## Troubleshooting

- **Unknown Item Error**: Verify that the barcode is correctly registered in the Item Barcode table
- **Scanning Issues**: Ensure the cursor is in the input field (automatic focus management should handle this)
- **Price Not Showing**: Check that the item has a price set in the selected price list

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## About the Developer

### Byoosi.com Limited

This application was designed and developed by **Byoosi.com Limited**, a leading technology solutions provider in Uganda specializing in ERPNext implementations and custom business solutions.

### Our Services

- **ERPNext Implementation & Support**: Full-service ERPNext setup, customization, and ongoing support
- **EFRIS Integration**: Seamless integration with Uganda's Electronic Fiscal Receipting and Invoicing Solution
- **Custom Applications**: Bespoke software development tailored to your business needs
- **Mobile Applications**: Cross-platform mobile app development for Android and iOS
- **E-Commerce Solutions**: Online store setup and integration with your ERP system
- **Business Process Automation**: Streamline your operations with custom workflows
- **Training & Consultation**: Expert guidance on digital transformation for your business

### Contact Information

- **Phone**: +256 779 728 077
- **Website**: [byoosi.com](https://byoosi.com)
- **Email**: info@byoosi.com

Looking for professional ERPNext services in Uganda? Contact us today for a consultation!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Metro Supermarket for the project requirements and branding
- Frappe Framework for the backend infrastructure
- All contributors who have helped improve this application