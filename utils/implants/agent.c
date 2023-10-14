#include <stdio.h>
#include <string.h>
#include <curl/curl.h>

#define LISTENER_IP "192.168.79.128"
#define LISTENER_PORT 10001
#define SECRET_KEY "PASSWORD"
#define URL "http://" LISTENER_IP ":" LISTENER_PORT "/tag"

size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    // Add callback processing here if you want to handle server response
    return realsize;  // Returning realsize ensures we've "handled" all the data
}

void register_with_listener() {
    CURL *curl;
    CURLcode res;
    char post_data[200];  // Ensure the buffer is large enough
    struct curl_slist *headers = NULL;

    sprintf(post_data, "{\"hostname\": \"your_host\", \"ip_address\": \"your_ip\", \"username\": \"your_user\"}");

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, URL);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);

        // Set headers
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, "X-Secret-Key: " SECRET_KEY);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);

        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);  // Free headers
    }

    curl_global_cleanup();
}

int main() {
    register_with_listener();
    return 0;
}
