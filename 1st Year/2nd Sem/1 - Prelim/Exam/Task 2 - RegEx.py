import re
from collections import Counter
import urllib.request
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading

class SocialMediaAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Metrics Analyzer")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📊 Social Media Metrics Analyzer", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # Input Section
        input_frame = tk.LabelFrame(self.root, text="Data Source", 
                                   font=('Arial', 11, 'bold'), 
                                   bg='#f0f0f0', padx=10, pady=10)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Radio buttons for source type
        self.source_type = tk.StringVar(value="url")
        
        radio_frame = tk.Frame(input_frame, bg='#f0f0f0')
        radio_frame.pack(fill='x', pady=5)
        
        tk.Radiobutton(radio_frame, text="URL", variable=self.source_type, 
                      value="url", font=('Arial', 10), bg='#f0f0f0',
                      command=self.toggle_source_type).pack(side='left', padx=10)
        
        tk.Radiobutton(radio_frame, text="Local File", variable=self.source_type, 
                      value="file", font=('Arial', 10), bg='#f0f0f0',
                      command=self.toggle_source_type).pack(side='left', padx=10)
        
        # Entry and buttons
        entry_frame = tk.Frame(input_frame, bg='#f0f0f0')
        entry_frame.pack(fill='x', pady=5)
        
        self.source_entry = tk.Entry(entry_frame, font=('Arial', 10), width=60)
        self.source_entry.pack(side='left', padx=5, ipady=5)
        self.source_entry.insert(0, "https://www.gutenberg.org/files/1342/1342-0.txt")
        
        self.browse_btn = tk.Button(entry_frame, text="Browse", 
                                    command=self.browse_file,
                                    font=('Arial', 9), state='disabled',
                                    bg='#95a5a6', fg='white', padx=10)
        self.browse_btn.pack(side='left', padx=5)
        
        # Analyze button
        self.analyze_btn = tk.Button(input_frame, text="🔍 Analyze Data", 
                                    command=self.start_analysis,
                                    font=('Arial', 11, 'bold'),
                                    bg='#27ae60', fg='white', 
                                    padx=20, pady=8, cursor='hand2')
        self.analyze_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(input_frame, mode='indeterminate', length=400)
        self.progress.pack(pady=5)
        
        # Results Section
        results_frame = tk.LabelFrame(self.root, text="Analysis Results", 
                                     font=('Arial', 11, 'bold'),
                                     bg='#f0f0f0', padx=10, pady=10)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     font=('Courier', 10),
                                                     wrap=tk.WORD,
                                                     bg='#ffffff',
                                                     fg='#2c3e50')
        self.results_text.pack(fill='both', expand=True)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  font=('Arial', 9), 
                                  bg='#34495e', fg='white',
                                  anchor='w', padx=10)
        self.status_bar.pack(side='bottom', fill='x')
        
    def toggle_source_type(self):
        """Toggle between URL and file input"""
        if self.source_type.get() == "file":
            self.browse_btn.config(state='normal', bg='#3498db')
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, "Click Browse to select a file...")
        else:
            self.browse_btn.config(state='disabled', bg='#95a5a6')
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, "https://www.gutenberg.org/files/1342/1342-0.txt")
    
    def browse_file(self):
        """Open file dialog to select a file"""
        filename = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, filename)
    
    def start_analysis(self):
        """Start analysis in a separate thread"""
        source = self.source_entry.get().strip()
        
        if not source:
            messagebox.showerror("Error", "Please enter a URL or select a file!")
            return
        
        # Disable button and start progress bar
        self.analyze_btn.config(state='disabled')
        self.progress.start(10)
        self.status_bar.config(text="Analyzing data...")
        self.results_text.delete(1.0, tk.END)
        
        # Run analysis in separate thread to keep UI responsive
        thread = threading.Thread(target=self.analyze_data, args=(source,))
        thread.daemon = True
        thread.start()
    
    def analyze_data(self, source):
        """Perform the actual analysis"""
        try:
            # Read data
            if self.source_type.get() == "url":
                content = self.read_from_url(source)
            else:
                content = self.read_from_file(source)
            
            if not content:
                self.display_error("Failed to load data from source.")
                return
            
            # Perform analysis
            results = self.perform_analysis(content)
            
            # Display results
            self.display_results(results)
            
        except Exception as e:
            self.display_error(f"Error during analysis: {str(e)}")
        
        finally:
            # Re-enable button and stop progress bar
            self.root.after(0, self.finish_analysis)
    
    def finish_analysis(self):
        """Clean up after analysis"""
        self.analyze_btn.config(state='normal')
        self.progress.stop()
        self.status_bar.config(text="Analysis complete!")
    
    def read_from_url(self, url):
        """Fetch content from URL"""
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
    
    def read_from_file(self, filename):
        """Read content from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Failed to read file: {str(e)}")
    
    def perform_analysis(self, content):
        """Analyze the content using regex"""
        # Extract patterns
        hashtags = re.findall(r'#\w+', content, re.IGNORECASE)
        mentions = re.findall(r'@\w+', content, re.IGNORECASE)
        urls = re.findall(r'https?://[^\s]+', content)
        posts = [post.strip() for post in content.split('\n') if post.strip()]
        
        # Analyze
        results = {
            'hashtags': {
                'total': len(hashtags),
                'unique': len(set(hashtags)),
                'top': Counter(hashtags).most_common(5) if hashtags else []
            },
            'mentions': {
                'total': len(mentions),
                'unique': len(set(mentions)),
                'top': Counter(mentions).most_common(5) if mentions else []
            },
            'urls': {
                'total': len(urls),
                'posts_with_urls': sum(1 for post in posts if re.search(r'https?://', post))
            },
            'posts': {
                'total': len(posts),
                'avg_length': sum(len(post) for post in posts) / len(posts) if posts else 0,
                'min_length': min(len(post) for post in posts) if posts else 0,
                'max_length': max(len(post) for post in posts) if posts else 0,
                'with_questions': len([p for p in posts if re.search(r'\?', p)]),
                'with_numbers': len([p for p in posts if re.search(r'\d+', p)])
            }
        }
        
        # Calculate averages
        if results['posts']['total'] > 0:
            results['avg_hashtags_per_post'] = results['hashtags']['total'] / results['posts']['total']
            results['avg_mentions_per_post'] = results['mentions']['total'] / results['posts']['total']
        else:
            results['avg_hashtags_per_post'] = 0
            results['avg_mentions_per_post'] = 0
        
        return results
    
    def display_results(self, results):
        """Display results in the text area"""
        output = []
        output.append("=" * 70)
        output.append("ANALYSIS RESULTS")
        output.append("=" * 70)
        output.append("")
        
        # Hashtag Analysis
        output.append("📌 HASHTAG ANALYSIS")
        output.append("-" * 70)
        output.append(f"Total hashtags found: {results['hashtags']['total']}")
        output.append(f"Unique hashtags: {results['hashtags']['unique']}")
        
        if results['hashtags']['top']:
            output.append("\nTop 5 Most Popular Hashtags:")
            for i, (tag, count) in enumerate(results['hashtags']['top'], 1):
                output.append(f"  {i}. {tag}: {count} times")
        output.append("")
        
        # Mentions Analysis
        output.append("👤 MENTIONS ANALYSIS")
        output.append("-" * 70)
        output.append(f"Total mentions found: {results['mentions']['total']}")
        output.append(f"Unique users mentioned: {results['mentions']['unique']}")
        
        if results['mentions']['top']:
            output.append("\nTop 5 Most Mentioned Users:")
            for i, (user, count) in enumerate(results['mentions']['top'], 1):
                output.append(f"  {i}. {user}: {count} times")
        output.append("")
        
        # URL Analysis
        output.append("🔗 URL ANALYSIS")
        output.append("-" * 70)
        output.append(f"Total URLs found: {results['urls']['total']}")
        output.append(f"Posts with URLs: {results['urls']['posts_with_urls']}")
        output.append("")
        
        # Post Statistics
        output.append("📝 POST STATISTICS")
        output.append("-" * 70)
        output.append(f"Total posts analyzed: {results['posts']['total']}")
        output.append(f"Average post length: {results['posts']['avg_length']:.2f} characters")
        output.append(f"Shortest post: {results['posts']['min_length']} characters")
        output.append(f"Longest post: {results['posts']['max_length']} characters")
        output.append(f"\nAverage hashtags per post: {results['avg_hashtags_per_post']:.2f}")
        output.append(f"Average mentions per post: {results['avg_mentions_per_post']:.2f}")
        output.append("")
        
        # Pattern Search
        output.append("🔍 PATTERN SEARCH")
        output.append("-" * 70)
        output.append(f"Posts with questions: {results['posts']['with_questions']}")
        output.append(f"Posts containing numbers: {results['posts']['with_numbers']}")
        output.append("")
        
        output.append("=" * 70)
        output.append("✅ ANALYSIS COMPLETE!")
        output.append("=" * 70)
        
        # Update UI in main thread
        self.root.after(0, lambda: self.results_text.insert(1.0, '\n'.join(output)))
    
    def display_error(self, message):
        """Display error message"""
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.status_bar.config(text="Error occurred"))

def main():
    root = tk.Tk()
    app = SocialMediaAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()