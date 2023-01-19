<h1 align="center"> Metaphor Based Search Engine </h1>  

Metaphor based search engine developed for information retrieval.  

## Prerequisites

* Python 3.8  
* Install the required dependencies using `pip install -r requirements.txt` 

## Run the Program

Go to the root folder of the project and open the command prompt. Then use the commands given below to run the program.

* **Navigate to API folder**  => `cd API`

* **Run**  => `flask --app main run`  

## User Interfaces

* **Landing Interface** 

![Landing Interface](./UI%20Screenshots/landing_interface.png?raw=true "Landing Interface")

* **Advanced Search** 

![Advanced Search](./UI%20Screenshots/advanced_search.png?raw=true "Advanced Search")  

* **Try a Combination** 

![Try a Combination](./UI%20Screenshots/try_a_combination.png?raw=true "Try a Combination")

* **Search Results** 

![Search Results](./UI%20Screenshots/search_results_1.png?raw=true "Search Results")

## Example Search Queries

* **Advanced Search**  
`Singer(s) : Sunil Edirisinghe, Musician : Rohana Weerasinghe, Target Domain : Girls`   

* **Try a Combination**   
`and => Source Domain : Moon, Target Domain : Girls`   
`or => Source Domain : Moon, Target Domain : Girls`   
`not => Singer(s) : Sunil Edirisinghe, Musician : Rohana Weerasinghe`  

* **Search without Keyword Idenification and Classification**    
`Sunil Edirisinghe`    
`නීල වළාවෙි..ඇගෙ පෙම් කතාව අසාගෙන වරෙන්`    

* **Search with Keyword Idenification and Classification**    
`Songs which have metaphors related to Love`    
`metaphor target_domain : Girls`    
`මව සම්බන්ධ අරුතක් ඇති metaphors ඇති ගීත`
