// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

using System;
using System.Diagnostics;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace QAClient
{
    class QAServiceAgent
    {
        const string Endpoint = "/knowledgebases/********-****-****-****-************/generateAnswer";
        const string Host = "https://******/qnamaker";
        const string Key = "********-****-****-****-************";
        const string ContentType = "application/json";
        // {"question":"<Your question>"}

        public static async Task<Answers> DoQuery(string question)
        {
            try
            {
                using (HttpClient hc = new HttpClient())
                {
                    hc.DefaultRequestHeaders.Add("authorization", "EndpointKey " + Key);
                    string jsonBody = CreateJsonBodyElement(question);
                    StringContent content = new StringContent(jsonBody, Encoding.UTF8, ContentType);
                    string uri = Host + Endpoint;
                    HttpResponseMessage resp = await hc.PostAsync(uri, content);
                    string json = await resp.Content.ReadAsStringAsync();
                    var ro = Newtonsoft.Json.JsonConvert.DeserializeObject<Answers>(json);
                    return ro;
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex.Message);
                return null;
            }
        }

        private static string CreateJsonBodyElement(string question)
        {
            string a = "{\"question\":\"" + question + "\"}";
            return a;
        }
    }
}
