from rest_framework.pagination import PageNumberPagination

class PositionPagination(PageNumberPagination):
    page_size = 2
class VotePagination(PageNumberPagination):
    page_size = 2
class VoterPagination(PageNumberPagination):
    page_size = 2
class CandidatePagination(PageNumberPagination):
    page_size = 2