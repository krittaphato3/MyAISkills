# Native Android / Kotlin (on-demand reference)

Load only for native Android tasks.

### Activity with ViewModel
```kotlin
class MainViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val data = repository.fetchData()
            _uiState.value = _uiState.value.copy(
                data = data,
                isLoading = false
            )
        }
    }
}

data class UiState(
    val isLoading: Boolean = false,
    val data: List<Item> = emptyList(),
    val error: String? = null
)
```

Rules: StateFlow + ViewModel, coroutines for async, instrumented test for critical flows.
