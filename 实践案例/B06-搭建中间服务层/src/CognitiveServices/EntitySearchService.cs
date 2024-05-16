// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;

namespace CognitiveMiddlewareService.CognitiveServices
{
    public class EntitySearchService : IEntitySearchService
    {
        const string SearchEntityEndpoint = "https://******/bing/v7.0/entities?mkt=en-US&q=";
        const string Key1 = "********************************";
        const string Key2 = "********************************";

        private readonly IHttpClientFactory httpClientFactory;

        public EntitySearchService(IHttpClientFactory cf)
        {
            this.httpClientFactory = cf;
        }

        public async Task<string> SearchEntityAsync(string query)
        {
            using (HttpClient hc = this.httpClientFactory.CreateClient())
            {
                string uri = SearchEntityEndpoint + query;
                string jsonResult = await Helper.MakeGetRequest(hc, uri, Key1);
                Debug.Write(jsonResult);
                return jsonResult;
            }
        }

    }
}
