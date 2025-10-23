"""
Wikipedia Integration for Heri-Science
Fetches accurate historical information from Wikipedia
"""

import requests
import re
from typing import Dict, Optional, List

class WikipediaIntegration:
    """
    Fetches historical information from Wikipedia API
    """
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/w/api.php"
        self.user_agent = "Heri-Science/1.0 (Educational Archaeological Platform)"
    
    def search_wikipedia(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search Wikipedia for relevant articles
        """
        params = {
            'action': 'opensearch',
            'search': query,
            'limit': limit,
            'namespace': 0,
            'format': 'json'
        }
        
        headers = {
            'User-Agent': self.user_agent
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Parse OpenSearch format: [query, [titles], [descriptions], [urls]]
            titles = data[1] if len(data) > 1 else []
            descriptions = data[2] if len(data) > 2 else []
            urls = data[3] if len(data) > 3 else []
            
            results = []
            for i in range(len(titles)):
                results.append({
                    'title': titles[i],
                    'description': descriptions[i] if i < len(descriptions) else '',
                    'url': urls[i] if i < len(urls) else ''
                })
            
            return results
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
    
    def get_article_summary(self, title: str) -> Optional[Dict]:
        """
        Get detailed summary of a Wikipedia article
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts|info|pageimages',
            'exintro': True,
            'explaintext': True,
            'inprop': 'url',
            'pithumbsize': 500
        }
        
        headers = {
            'User-Agent': self.user_agent
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            if not pages:
                return None
            
            # Get the first (and should be only) page
            page_id = list(pages.keys())[0]
            if page_id == '-1':  # Page not found
                return None
            
            page = pages[page_id]
            
            return {
                'title': page.get('title', ''),
                'extract': page.get('extract', ''),
                'url': page.get('fullurl', ''),
                'thumbnail': page.get('thumbnail', {}).get('source', '')
            }
        except Exception as e:
            print(f"Wikipedia article fetch error: {e}")
            return None
    
    def get_artifact_info(self, artifact_name: str, civilization: str = None) -> Dict:
        """
        Get comprehensive information about an artifact
        """
        # Build search query
        search_query = artifact_name
        if civilization:
            search_query = f"{civilization} {artifact_name}"
        
        # Search for relevant articles
        search_results = self.search_wikipedia(search_query, limit=3)
        
        if not search_results:
            return {
                'found': False,
                'message': 'No Wikipedia information found for this artifact.'
            }
        
        # Get detailed info from the top result
        top_result = search_results[0]
        article = self.get_article_summary(top_result['title'])
        
        if not article:
            return {
                'found': False,
                'message': 'Could not retrieve detailed information.'
            }
        
        # Clean and format the extract
        extract = self._clean_extract(article['extract'])
        
        return {
            'found': True,
            'title': article['title'],
            'summary': extract,
            'url': article['url'],
            'thumbnail': article['thumbnail'],
            'related_articles': search_results[1:] if len(search_results) > 1 else []
        }
    
    def get_civilization_info(self, civilization: str) -> Dict:
        """
        Get information about a specific civilization
        """
        article = self.get_article_summary(civilization)
        
        if not article:
            # Try alternative search
            search_results = self.search_wikipedia(f"{civilization} civilization", limit=1)
            if search_results:
                article = self.get_article_summary(search_results[0]['title'])
        
        if not article:
            return {
                'found': False,
                'message': f'No Wikipedia information found for {civilization}.'
            }
        
        extract = self._clean_extract(article['extract'])
        
        return {
            'found': True,
            'title': article['title'],
            'summary': extract,
            'url': article['url'],
            'thumbnail': article['thumbnail']
        }
    
    def get_historical_period_info(self, period: str, region: str = None) -> Dict:
        """
        Get information about a historical period
        """
        search_query = period
        if region:
            search_query = f"{period} {region}"
        
        search_results = self.search_wikipedia(search_query, limit=1)
        
        if not search_results:
            return {
                'found': False,
                'message': f'No information found for period: {period}'
            }
        
        article = self.get_article_summary(search_results[0]['title'])
        
        if not article:
            return {
                'found': False,
                'message': 'Could not retrieve detailed information.'
            }
        
        extract = self._clean_extract(article['extract'])
        
        return {
            'found': True,
            'title': article['title'],
            'summary': extract,
            'url': article['url'],
            'thumbnail': article['thumbnail']
        }
    
    def _clean_extract(self, text: str, max_length: int = 800) -> str:
        """
        Clean and format Wikipedia extract
        """
        if not text:
            return ""
        
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n\n', text)
        
        # Truncate to max length at sentence boundary
        if len(text) > max_length:
            text = text[:max_length]
            # Find last complete sentence
            last_period = text.rfind('.')
            if last_period > max_length * 0.7:  # At least 70% of text
                text = text[:last_period + 1]
            text += "..."
        
        return text.strip()
    
    def format_response_with_wikipedia(self, query: str, wikipedia_data: Dict) -> str:
        """
        Format chatbot response with Wikipedia information
        """
        if not wikipedia_data.get('found'):
            return wikipedia_data.get('message', 'Information not available.')
        
        response = f"""**{wikipedia_data['title']}**

{wikipedia_data['summary']}

📚 **Source:** [Wikipedia]({wikipedia_data['url']})

*This information is sourced from Wikipedia and may require verification for academic use.*
"""
        
        # Add related articles if available
        if wikipedia_data.get('related_articles'):
            response += "\n\n**Related Topics:**\n"
            for article in wikipedia_data['related_articles'][:3]:
                response += f"- [{article['title']}]({article['url']})\n"
        
        return response


# Create global instance
wikipedia_integration = WikipediaIntegration()

def get_wikipedia_info(query: str, artifact_type: str = 'artifact', context: dict = None):
    """
    Get Wikipedia information based on query type
    """
    if context:
        civilization = context.get('civilization')
        period = context.get('period')
        
        if artifact_type == 'civilization' and civilization:
            return wikipedia_integration.get_civilization_info(civilization)
        elif artifact_type == 'period' and period:
            return wikipedia_integration.get_historical_period_info(period)
        else:
            # Get artifact info
            artifact_name = context.get('artifact_type', query)
            return wikipedia_integration.get_artifact_info(artifact_name, civilization)
    else:
        # General search
        search_results = wikipedia_integration.search_wikipedia(query, limit=1)
        if search_results:
            return wikipedia_integration.get_article_summary(search_results[0]['title'])
        return {'found': False, 'message': 'No information found.'}


if __name__ == "__main__":
    # Test the integration
    wiki = WikipediaIntegration()
    
    print("Testing Wikipedia Integration...")
    print("\n1. Searching for 'Egyptian Pyramid':")
    result = wiki.get_artifact_info("Pyramid", "Egyptian")
    print(f"Found: {result['found']}")
    if result['found']:
        print(f"Title: {result['title']}")
        print(f"Summary: {result['summary'][:200]}...")
    
    print("\n2. Getting civilization info:")
    result = wiki.get_civilization_info("Ancient Egypt")
    print(f"Found: {result['found']}")
    if result['found']:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")


