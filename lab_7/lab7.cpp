#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>
#include <string>
#include <ctime>
#include <condition_variable>


//global variables for whole programm
using namespace std;
condition_variable cv;      
bool ready_to_sell = false;  
int TOTAL_TICKETS = 250;
mutex ticket_mutex;

//struct of thread
struct ThreadData {
    int id;
    string movie_title;
	string date_time;
};

//function for running the thread
void SellTickets_6(ThreadData data) {
	//prinitng while starting the thread
    cout << "Seller " << data.id << " started a movie : " << data.movie_title << " at " << data.date_time << endl;

    while(true) {
		//getting current time adn date
        ticket_mutex.lock();
		
		time_t now = time(0);
		string dt =ctime(&now);
		dt.pop_back();
		
		data.date_time = dt;

        if (TOTAL_TICKETS <= 0) {
            ticket_mutex.unlock();
            break;
        }

        TOTAL_TICKETS--;
		//selling the ticket
        cout << "Seller " << data.id << " sold a ticket.  Remaining : " << TOTAL_TICKETS << " time check " << data.date_time<<endl;
		 ticket_mutex.unlock();
		 
        this_thread::sleep_for(chrono::milliseconds(50));

       
    }
}

void SellTickets_7(ThreadData data) {
    cout << "Seller " << data.id << " started: " << data.movie_title << endl;

    while (true) {
        unique_lock<mutex> lock(ticket_mutex);

        // Wait for the start signal AND ensure there are tickets left 
        cv.wait(lock, [] { return ready_to_sell || TOTAL_TICKETS <= 0; });

        if (TOTAL_TICKETS <= 0) break; // Safe exit

        // Update time and sell ticket
        time_t now = time(0);
        string dt = ctime(&now);
        dt.pop_back();
        
        TOTAL_TICKETS--;
        cout << "Seller " << data.id << " sold ticket. Remaining: " << TOTAL_TICKETS << " at " << data.date_time << endl;

        // Manual unlock before sleeping 
        lock.unlock(); 
        this_thread::sleep_for(chrono::milliseconds(50)); 
    }
}

int main() { 
    const int num_threads = 6;
    vector<thread> threads;
	string title[6] = {"Star Wars", "Barbie", "Openheimer", "Car 1", "Car 2", "Car 3"};
	
	//---------------------------LAB 6----------------------
    auto start_time6 = chrono::high_resolution_clock::now();

    for (int i = 0; i < num_threads; ++i){
		//getting current time adn date
		time_t now = time(0);
		string dt =ctime(&now);
		dt.pop_back();
		
		
        ThreadData data = {i + 1, title[i], dt}; 
        
        threads.push_back(thread(SellTickets_6, data));
    }

    for (auto& th : threads){
        th.join();
    }
	
	//claculating the time of running the porgramm

    auto end_time6 = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed6 = end_time6 - start_time6;

    cout << "\nAll Tickets sold lab6" << endl;
    cout << "Execution time for lab6: " << elapsed6.count() << " sec" << endl;
	
	//---------------------------LAB 7----------------------
	threads.clear();
    TOTAL_TICKETS = 250;  
    ready_to_sell = false;
	auto start_time7 = chrono::high_resolution_clock::now();
    
    for(int i = 0; i < num_threads; i++) {
		//getting current time adn date
        time_t now = time(0);
        string dt = ctime(&now);
        dt.pop_back();
        
        ThreadData data = {i + 1, title[i], dt}; 
        
        threads.push_back(thread(SellTickets_7, data));
    }

    {
        lock_guard<mutex> lock(ticket_mutex); 
        ready_to_sell = true;          
    }
	
    cv.notify_all();

    for (auto& th : threads){
        th.join();
    }
	
	//claculating the time of running the porgramm
    auto end_time7 = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed7 = end_time7 - start_time7;

    cout << "\nAll Tickets sold (Lab 7 with CV)" << endl;
    cout << "Execution time for lab7: " << elapsed7.count() << " sec" << endl;
	
    return 0; 
}