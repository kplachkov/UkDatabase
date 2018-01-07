from datetime import datetime

# from nltk import word_tokenize, re
# from nltk.corpus import stopwords

from UkDatabaseAPI.database.query_builder.query_builder import QueryBuilder

POST_PUB_DATE = "POST_PUB_DATE"
TEXT = "TEXT"
"""str: Keys in MongoBD."""


class MongoQueryBuilder(QueryBuilder):
    @staticmethod
    def get_query_for_search_by_text(text: str) -> dict:
        """Get MongoDB query for searching by text.
        Args:
            text: The text search criterion, from the URL argument.
        Returns:
            MongoDB query for finding posts containing the text.
        """

        # Uncomment and use the following code if you have problems creating text index!

        # stop_words = set(stopwords.words('english'))  # Commonly used words. Example: 'or', 'as', 'but'...
        # word_tokens = word_tokenize(text)  # List of words from the text.
        # filtered_sentence = [w for w in word_tokens if w not in stop_words]  # List without commonly used words
        # regex = r"\s|\s".join(filtered_sentence)
        # regex = r"\s" + regex + r"\s"  # Example: r"\sword1\s|\sword2\s|\sword3\s"
        # return {TEXT: {"$regex": re.compile(regex, re.IGNORECASE)}}

        return {"$text": {"$search": text}}

    @staticmethod
    def get_query_for_search_by_post_date(date: str) -> dict:
        """Get MongoDB query for searching by date or time range.
        Args:
            date: The date or time range search criterion, from the URL argument.
        Returns:
            MongoDB query for finding posts published within a specific time range or on a date.
        """
        if "-" in date:
            start_date = ""
            end_date = ""
            if date.startswith("-"):
                end_date = date[1:]
            elif date.endswith("-"):
                start_date = date[:-1]
            else:
                start_date, end_date = date.split("-")  # Split into start and end date.
                start_date = start_date.strip()
                end_date = end_date.strip()
            # Check if dates are provided.
            assert (start_date or end_date), "Please provide a date with the following format: %d/%m/%Y (31/12/2017)"
            start_date_obj = None
            end_date_obj = None
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")  # String format to datetime.
                except Exception as e:
                    print("Exception:", e)
                    raise AssertionError("Please use the following date format: %d/%m/%Y (31/12/2017)")
            if end_date:
                try:
                    end_date_obj = datetime.strptime(end_date, "%d/%m/%Y")  # String format to datetime.
                except Exception as e:
                    print("Exception:", e)
                    raise AssertionError("Please use the following date format: %d/%m/%Y (31/12/2017)")
            if start_date_obj and not end_date_obj:
                # Return a query for finding posts after the provided date.
                return {POST_PUB_DATE: {"$gte": start_date_obj}}
            elif not start_date_obj and end_date_obj:
                # Return a query for finding posts before the provided date.
                return {POST_PUB_DATE: {"$lt": end_date_obj}}
            elif start_date_obj and end_date_obj:
                # Check if dates are in order.
                assert (start_date_obj < end_date_obj), "The first date must be lower than the second."
                # Return a query for finding posts between the provided dates.
                return {POST_PUB_DATE: {
                    "$gte": start_date_obj,
                    "$lt": end_date_obj
                }}
        else:
            try:
                # Return a query for finding posts published on the date.
                post_pub_date: datetime = datetime.strptime(date, "%d/%m/%Y")
                return {POST_PUB_DATE: post_pub_date}
            except Exception as e:
                print("Exception:", e)
                raise AssertionError("Please use the following date format: %d/%m/%Y (31/12/2017)")
