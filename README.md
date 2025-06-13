# Email Processor AI

A production-grade Python application for intelligently processing email order requests and customer inquiries for a fashion store. The application uses advanced Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) and vector store techniques to handle various types of customer communications.

## Features

- **Email Classification**: Automatically classifies emails as either order requests or product inquiries
- **Order Processing**: Validates orders against product catalog and stock levels
- **Product Inquiries**: Handles customer questions using RAG to retrieve relevant product information
- **Response Generation**: Creates professional, context-aware email responses
- **Stock Management**: Tracks and updates product stock levels
- **Logging**: Comprehensive logging for monitoring and debugging

## Project Structure

```
email_processor_ai/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── data/                  # Data directory
│   ├── products.csv      # Product catalog
│   └── emails.csv        # Input emails
├── modules/              # Core functionality modules
│   ├── classifier.py     # Email classification
│   ├── order_processor.py # Order handling
│   ├── inquiry_handler.py # Product inquiry handling
│   ├── response_generator.py # Response formatting
│   └── rag_utils.py      # RAG utilities
├── outputs/              # Output directory
│   ├── email-classification.csv
│   ├── order-status.csv
│   ├── order-response.csv
│   └── inquiry-response.csv
├── requirements.txt      # Project dependencies
└── utils/               # Utility modules
    ├── spreadsheet_io.py # Google Sheets integration
    └── logger.py        # Logging utilities
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd email_processor_ai
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Create a .env file with:
   OPENAI_API_KEY=your_api_key
   ```

## Usage

1. Prepare your input data:
   - Place your product catalog in `data/products.csv`
   - Place your email data in `data/emails.csv`

2. Run the application:
   ```bash
   python main.py
   ```

3. Check the outputs:
   - Email classifications: `outputs/email-classification.csv`
   - Order status: `outputs/order-status.csv`
   - Order responses: `outputs/order-response.csv`
   - Inquiry responses: `outputs/inquiry-response.csv`

## Input Data Format

### Products CSV
- `product_id`: Unique identifier
- `name`: Product name
- `category`: Product category
- `description`: Detailed description
- `season`: Season availability
- `stock`: Current stock level

### Emails CSV
- `email_id`: Unique identifier
- `subject`: Email subject
- `body`: Email content

## Output Data Format

### Email Classification
- `email_id`: Email identifier
- `category`: Classification result ("order_request" or "product_inquiry")

### Order Status
- `email_id`: Email identifier
- `product_id`: Product identifier
- `quantity`: Requested quantity
- `status`: Order status ("created" or "out_of_stock")

### Order Response
- `email_id`: Email identifier
- `response`: Generated response email

### Inquiry Response
- `email_id`: Email identifier
- `response`: Generated response email

## Limitations and Future Improvements

1. **Google Sheets Integration**: Currently saves to CSV files for manual upload. Future versions will implement direct Google Sheets API integration.

2. **Error Handling**: Enhanced error handling and recovery mechanisms.

3. **Performance Optimization**: Implement batch processing for large email volumes.

4. **Testing**: Add comprehensive unit tests and integration tests.

5. **API Rate Limiting**: Implement rate limiting for API calls.

6. **Monitoring**: Add monitoring and alerting capabilities.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
