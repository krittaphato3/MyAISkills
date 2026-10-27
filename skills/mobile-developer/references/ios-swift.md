# Native iOS / Swift (on-demand reference)

Load only for native iOS tasks.

### SwiftUI View
```swift
import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()

    var body: some View {
        NavigationView {
            List(viewModel.items) { item in
                NavigationLink(destination: DetailView(item: item)) {
                    Text(item.title)
                }
            }
            .navigationTitle("Items")
            .onAppear {
                viewModel.loadItems()
            }
        }
    }
}

class ContentViewModel: ObservableObject {
    @Published var items: [Item] = []

    func loadItems() {
        // Fetch items
    }
}
```

Rules: SwiftUI + ObservableObject, async/await for async, XCTest + XCUITest for critical flows.
