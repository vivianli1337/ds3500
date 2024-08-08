# import libraries & class
from nlp_library import NLPLibrary


def main():
    # Instantiate NLPLibrary object
    library = NLPLibrary()

    # Load stop words
    library.load_stop_words("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/stopwords.txt")

    # Load text files
    # https://www.wsj.com/tech/ai/the-fight-for-ai-talent-pay-million-dollar-packages-and-buy-whole-teams-c370de2b?mod=ai_more_article_pos2
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text1.txt",
                      label="1. The Fight for AI Talent: Pay Million-Dollar Packages and Buy Whole Teams")

    # https://www.wsj.com/tech/ai/jobs-chatgpt-artificial-intelligence-openai-cea961d5?mod=ai_more_article_pos8
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text2.txt",
                      label="2. Want to Know if AI Will Take Your Job? I Tried Using It to Replace Myself")

    # https://www.wsj.com/tech/ai/super-micro-computer-company-profile-d93a41da?mod=ai_more_article_pos26
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text3.txt",
                      label="3. Meet the Tech Company That Had a Better Year Than Nvidia")

    # https://www.wsj.com/tech/drone-swarms-are-about-to-change-the-balance-of-military-power-e091aa6f?mod=ai_more_article_pos28
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text4.txt",
                      label="4. Drone Swarms Are About to Change the Balance of Military Power")

    # https://www.wsj.com/tech/ai/as-generative-ai-takes-off-researchers-warn-of-data-poisoning-d394385c?mod=ai_more_article_pos29
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text5.txt",
                      label="5. As Generative AI Takes Off, Researchers Warn of Data Poisoning")

    # https://www.wsj.com/articles/openais-not-so-secret-weapon-in-winning-business-customers-chatgpt-06aca11c
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text6.txt",
                      label="6. OpenAI’s Not-So-Secret Weapon in Winning Business Customers? ChatGPT")

    # https://www.wsj.com/articles/how-the-ad-industry-is-making-ai-images-look-less-like-ai-8b4250fd?mod=ai_more_article_pos6
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text7.txt",
                      label="7. How the Ad Industry Is Making AI Images Look Less Like AI")

    # https://www.wsj.com/tech/ai/generative-ai-mba-business-school-13199631?mod=ai_more_article_pos3
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text8.txt",
                      label="8. Business Schools Are Going All In on AI")

    # https://www.wsj.com/tech/ai/ai-training-data-synthetic-openai-anthropic-9230f8d8?mod=ai_more_article_pos10
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text9.txt",
                      label="9. For Data-Guzzling AI Companies, the Internet Is Too Small")

    # https://www.wsj.com/articles/open-source-companies-are-sharing-their-ai-free-can-they-crack-openais-dominance-26149e9c?mod=ai_more_article_pos32
    library.load_text("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw7/text10.txt",
                      label="10. Open-Source Companies Are Sharing Their AI Free. Can They Crack OpenAI’s Dominance?")

    # Generate visualizations
    library.wordcount_sankey(k=10)
    library.word_cloud_subplots()
    library.word_frequency_overlay()


if __name__ == "__main__":
    main()
