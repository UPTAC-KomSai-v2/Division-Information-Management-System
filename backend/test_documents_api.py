"""
Quick test script for Document Management System API
Run this after starting the Django server: python manage.py runserver
"""
import requests
import json
import os
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "admin@test.com"
TEST_PASSWORD = "testpass123"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_login():
    """Test user login and get JWT token"""
    print_section("1. Testing Login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access")
            print(f"✓ Login successful!")
            print(f"✓ Token received: {token[:30]}...")
            return token
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to server at {BASE_URL}")
        print(f"  Make sure Django server is running: python manage.py runserver")
        return None
    except Exception as e:
        print(f"✗ Error during login: {e}")
        return None

def test_list_documents(token):
    """Test listing documents"""
    print_section("2. Testing List Documents")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            documents = response.json()
            print(f"✓ List documents successful!")
            print(f"✓ Found {len(documents)} document(s)")
            
            if documents:
                print(f"\n  Documents:")
                for doc in documents[:5]:  # Show first 5
                    print(f"    - ID: {doc.get('id')}, Name: {doc.get('name')}")
            
            return True
        else:
            print(f"✗ Failed to list documents: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error listing documents: {e}")
        return False

def test_upload_document(token):
    """Test uploading a document"""
    print_section("3. Testing Upload Document")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test file
    test_file_path = Path("test_document.txt")
    try:
        with open(test_file_path, "w") as f:
            f.write("This is a test document content for API testing.\n")
            f.write("Created automatically by test script.")
        print(f"✓ Test file created: {test_file_path}")
    except Exception as e:
        print(f"✗ Cannot create test file: {e}")
        return None
    
    # Prepare upload data
    data = {
        "name": "Test Document from Script",
        "document_type": "MEMOS",
        "access_level": "PUBLIC",
        "description": "Automatically uploaded by test script"
    }
    
    files = {
        "file": ("test_document.txt", open(test_file_path, "rb"), "text/plain")
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            data=data,
            files=files,
            timeout=10
        )
        
        files["file"][1].close()  # Close the file
        
        if response.status_code == 201:
            doc_data = response.json()
            doc_id = doc_data.get("id")
            print(f"✓ Document uploaded successfully!")
            print(f"✓ Document ID: {doc_id}")
            print(f"✓ Name: {doc_data.get('name')}")
            print(f"✓ Type: {doc_data.get('document_type')}")
            print(f"✓ Access: {doc_data.get('access_level')}")
            return doc_id
        else:
            print(f"✗ Upload failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error uploading document: {e}")
        return None
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()

def test_get_document(token, doc_id):
    """Test getting document details"""
    print_section(f"4. Testing Get Document Details (ID: {doc_id})")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/{doc_id}/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            doc_data = response.json()
            print(f"✓ Document retrieved successfully!")
            print(f"  ID: {doc_data.get('id')}")
            print(f"  Name: {doc_data.get('name')}")
            print(f"  File URL: {doc_data.get('file_url', 'N/A')}")
            print(f"  File Size: {doc_data.get('file_size', 0)} bytes")
            print(f"  Uploaded by: {doc_data.get('uploaded_by_email', 'N/A')}")
            return True
        else:
            print(f"✗ Failed to get document: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error getting document: {e}")
        return False

def test_search_documents(token):
    """Test searching documents"""
    print_section("5. Testing Search Documents")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/?search=Test",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            documents = response.json()
            print(f"✓ Search successful!")
            print(f"✓ Found {len(documents)} document(s) matching 'Test'")
            return True
        else:
            print(f"✗ Search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error searching documents: {e}")
        return False

def test_filter_documents(token):
    """Test filtering documents"""
    print_section("6. Testing Filter Documents")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/?type=MEMOS&access=PUBLIC",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            documents = response.json()
            print(f"✓ Filter successful!")
            print(f"✓ Found {len(documents)} document(s) with type=MEMOS and access=PUBLIC")
            return True
        else:
            print(f"✗ Filter failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error filtering documents: {e}")
        return False

def test_download_document(token, doc_id):
    """Test downloading a document"""
    print_section(f"7. Testing Download Document (ID: {doc_id})")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/{doc_id}/download/",
            headers=headers,
            timeout=10,
            stream=True
        )
        
        if response.status_code == 200:
            content_length = len(response.content)
            print(f"✓ Download successful!")
            print(f"✓ File size: {content_length} bytes")
            print(f"✓ Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            return True
        else:
            print(f"✗ Download failed: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ Error downloading document: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Document Management System - API Test Suite")
    print("="*60)
    print(f"\nTesting server at: {BASE_URL}")
    print(f"Test user: {TEST_EMAIL}")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=2)
    except:
        print(f"\n✗ ERROR: Cannot connect to server at {BASE_URL}")
        print(f"\n  Please start the Django server first:")
        print(f"    cd Division-Information-Management-System/backend")
        print(f"    python manage.py runserver")
        sys.exit(1)
    
    results = []
    
    # Test 1: Login
    token = test_login()
    if not token:
        print("\n✗ Cannot continue without authentication token")
        print("  Please check your credentials and server configuration")
        sys.exit(1)
    
    # Test 2: List documents
    results.append(("List Documents", test_list_documents(token)))
    
    # Test 3: Upload document
    doc_id = test_upload_document(token)
    if doc_id:
        results.append(("Upload Document", True))
        
        # Test 4: Get document
        results.append(("Get Document", test_get_document(token, doc_id)))
        
        # Test 5: Search
        results.append(("Search Documents", test_search_documents(token)))
        
        # Test 6: Filter
        results.append(("Filter Documents", test_filter_documents(token)))
        
        # Test 7: Download
        results.append(("Download Document", test_download_document(token, doc_id)))
    else:
        results.append(("Upload Document", False))
    
    # Print summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Document Management System is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

