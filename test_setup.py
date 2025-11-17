"""Test script to verify AIscribe setup and API connections"""

import sys
from logger_config import setup_logger

logger = setup_logger()

def test_imports():
    """Test if all required packages are installed"""
    logger.info("Testing imports...")
    
    try:
        import flask
        logger.info(f"✓ Flask version: {flask.__version__}")
    except ImportError:
        logger.error("✗ Flask not installed")
        return False
    
    try:
        import assemblyai
        logger.info(f"✓ AssemblyAI installed")
    except ImportError:
        logger.error("✗ AssemblyAI not installed")
        return False
    
    try:
        import openai
        logger.info(f"✓ OpenAI library installed")
    except ImportError:
        logger.error("✗ OpenAI library not installed")
        return False
    
    try:
        import requests
        logger.info(f"✓ Requests library installed")
    except ImportError:
        logger.error("✗ Requests library not installed")
        return False
    
    return True

def test_config():
    """Test if configuration is set up correctly"""
    logger.info("\nTesting configuration...")
    
    try:
        from config import ASSEMBLYAI_API_KEY, OPENROUTER_API_KEY, PRIMARY_MODEL, FALLBACK_MODEL
        
        if ASSEMBLYAI_API_KEY and len(ASSEMBLYAI_API_KEY) > 10:
            logger.info("✓ AssemblyAI API key configured")
        else:
            logger.warning("⚠ AssemblyAI API key might be invalid")
        
        if OPENROUTER_API_KEY and len(OPENROUTER_API_KEY) > 10:
            logger.info("✓ OpenRouter API key configured")
        else:
            logger.warning("⚠ OpenRouter API key might be invalid")
        
        logger.info(f"✓ Primary Model: {PRIMARY_MODEL}")
        logger.info(f"✓ Fallback Model: {FALLBACK_MODEL}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Configuration error: {str(e)}")
        return False

def test_services():
    """Test if services can be initialized"""
    logger.info("\nTesting service initialization...")
    
    try:
        from transcription_service import TranscriptionService
        service = TranscriptionService()
        logger.info("✓ TranscriptionService initialized")
    except Exception as e:
        logger.error(f"✗ TranscriptionService failed: {str(e)}")
        return False
    
    try:
        from ai_summarization_service import AISummarizationService
        service = AISummarizationService()
        logger.info("✓ AISummarizationService initialized")
    except Exception as e:
        logger.error(f"✗ AISummarizationService failed: {str(e)}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    logger.info("\nTesting directories...")
    
    import os
    
    directories = ['uploads', 'templates', 'static']
    
    for directory in directories:
        if os.path.exists(directory):
            logger.info(f"✓ {directory}/ directory exists")
        else:
            logger.warning(f"⚠ {directory}/ directory not found")
            os.makedirs(directory, exist_ok=True)
            logger.info(f"✓ Created {directory}/ directory")
    
    return True

def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("AIscribe Setup Test")
    logger.info("=" * 60 + "\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Services", test_services),
        ("Directories", test_directories),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    logger.info("=" * 60)
    
    if all_passed:
        logger.info("\n✅ All tests passed! AIscribe is ready to use.")
        logger.info("Run 'python app.py' to start the application.")
        return 0
    else:
        logger.error("\n❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())



